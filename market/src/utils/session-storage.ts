function setSession(key: string, value: string) {
  sessionStorage.setItem(key, value)
}

function getSession(key: string) {
  return sessionStorage.getItem(key)
}

function clearSession() {
  sessionStorage.clear()
}

export { setSession, getSession, clearSession }
