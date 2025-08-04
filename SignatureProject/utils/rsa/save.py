from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from SignatureProject.settings import BASE_DIR

def save_keys(private, public, user_name):
    private_pem = private.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )
    public_pem = public.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    import os
    user_dir = BASE_DIR / user_name
    os.makedirs(user_dir, exist_ok=True)
    with open(user_dir / "private_key.pem", "wb") as f:
        f.write(private_pem)
    with open(user_dir / "public_key.pem", "wb") as f:
        f.write(public_pem)
