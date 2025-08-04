import hashlib
import datetime
import os
import json
import base64
from pathlib import Path
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.serialization import load_pem_private_key, load_pem_public_key

def read_text_file(file):
    """
    Read the content of a text file
    
    Args:
        file: File object or path to file
    
    Returns:
        str: Content of the file
    """
    if hasattr(file, 'read'):
        # It's a file-like object
        return file.read().decode('utf-8')
    else:
        # It's a path
        with open(file, 'r', encoding='utf-8') as f:
            return f.read()

def calculate_hash(content):
    """
    Calculate SHA-256 hash of content
    
    Args:
        content: String content to hash
    
    Returns:
        bytes: SHA-256 hash
    """
    return hashlib.sha256(content.encode('utf-8')).digest()

def load_private_key(username):
    """
    Load private key for a user
    
    Args:
        username: Username to load key for
    
    Returns:
        RSAPrivateKey: The loaded private key
    """
    key_path = Path(f"{username}/private_key.pem")
    
    if not os.path.exists(key_path):
        raise FileNotFoundError(f"Private key not found for user {username}")
    
    with open(key_path, 'rb') as key_file:
        private_key = load_pem_private_key(
            key_file.read(),
            password=None
        )
    
    return private_key

def load_public_key(username):
    """
    Load public key for a user
    
    Args:
        username: Username to load key for
    
    Returns:
        RSAPublicKey: The loaded public key
    """
    key_path = Path(f"{username}/public_key.pem")
    
    if not os.path.exists(key_path):
        raise FileNotFoundError(f"Public key not found for user {username}")
    
    with open(key_path, 'rb') as key_file:
        public_key = load_pem_public_key(
            key_file.read(),
            password=None
        )
    
    return public_key

def sign_document(content, username):
    """
    Sign document content with user's private key
    
    Args:
        content: Document content to sign
        username: Username whose private key to use
    
    Returns:
        tuple: (signature bytes, timestamp)
    """
    # Calculate hash of content
    content_hash = calculate_hash(content)
    
    # Load private key
    private_key = load_private_key(username)
    
    # Sign the hash
    signature = private_key.sign(
        content_hash,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )
    
    # Get current timestamp
    timestamp = datetime.datetime.now().isoformat()
    
    return signature, timestamp

def save_signature(signature, timestamp, file_name, username):
    """
    Save signature to a .sig file with timestamp and store metadata in JSON
    Ensures each user can only sign a specific document once
    
    Args:
        signature: Signature bytes
        timestamp: Timestamp string
        file_name: Original file name
        username: Username who signed
    
    Returns:
        str: Path to signature file or None if user already signed this document
    """
    
    # Store signature metadata in JSON file
    json_path = "signature.json"
    base_name = os.path.basename(file_name)
    
    try:
        # Read existing data if file exists
        if os.path.exists(json_path):
            with open(json_path, 'r') as json_file:
                signatures = json.load(json_file)
        else:
            signatures = []
        
        # Check if user already signed this specific document
        for entry in signatures:
            if entry["user"] == username and entry["file"] == base_name:
                print(f"User {username} has already signed document {base_name}")
                return None
        
        # Create signatures directory if it doesn't exist
        os.makedirs('signatures', exist_ok=True)
        
        # Generate signature file name
        sig_file = f"signatures/{base_name}_{username}_{timestamp.replace(':', '-')}.sig"
        
        # Write signature to binary file
        with open(sig_file, 'wb') as f:
            f.write(signature)
        
        # Add new signature entry
        signatures.append({
            "user": username,
            "timestamp": timestamp,
            "file": base_name,
            "signature": base64.b64encode(signature).decode('utf-8')
        })
        
        # Write updated data back to file
        with open(json_path, 'w') as json_file:
            json.dump(signatures, json_file, indent=2)
            
        return sig_file
            
    except Exception as e:
        print(f"Error saving signature to JSON: {e}")
        return None

def verify_signature(username, file_path, signature_path):
    """
    Verify a signature against a document file
    
    Args:
        username: Username whose public key to use for verification
        file_path: Path to the original document file
        signature_path: Path to the .sig file containing the signature
    
    Returns:
        bool: True if signature is valid, False otherwise
    """
    try:
        # Read the file content
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            
        # Calculate hash of content
        content_hash = calculate_hash(content)
        
        # Load the signature from file
        sig_path = Path(signature_path)
        with open(sig_path, 'rb') as f:
            signature = f.read()
        
        # Load the public key from register.json
        register_path = Path("register.json")
        if not os.path.exists(register_path):
            print("User registry not found")
            return False
            
        with open(register_path, "r") as file:
            users = json.load(file)
            
        if username not in users:
            print(f"User {username} not found in registry")
            return False
            
        # Get the public key PEM string
        public_key_pem = users[username]
        
        # Load the public key
        public_key = load_pem_public_key(public_key_pem.encode('utf-8'))
        
        # Verify the signature
        public_key.verify(
            signature,
            content_hash,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        
        # If we get here without an exception, the signature is valid
        print(f"Signature is valid for document {file_path}")
        return True
        
    except Exception as e:
        print(f"Signature verification failed: {e}")
        return False