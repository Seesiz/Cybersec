def verify_signature(username, file_path, signature_path):
    register_path = Path("register.json")
    try:
        # Check if file exists
        if os.path.exists(register_path):
            with open(register_path, "r") as file:
                data = json.load(file)
        else:
            # Create new data structure if file doesn't exist
            data = {}
        
        # Check if user already exists
        if not username in data:
            print(f"User {username} does not exist!")
            return False
        
        public_key = data[username]
        
        with open(signature_path, "r") as file:
            signature = json.load(file)

        ##find signature in signature.json by username & file name
        for entry in signature:
            if entry["user"] == username and entry["file"] == file_path:
                signature = entry["signature"]
                break
        
        public_key.verify(
            signature,
            hash_value,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        
    except Exception as e:
        print(f"Error registering user: {e}")
        return False
   

