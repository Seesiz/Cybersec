import json
import os
from pathlib import Path

def register_user(username, public_key):
    # Path to the register file
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
        if username in data:
            print(f"User {username} already exists!")
            return False
        
        # Add the new user to the dictionary
        data[username] = public_key
        
        # Write back to file
        with open(register_path, "w") as file:
            json.dump(data, file, indent=2)
            
        print(f"User {username} registered successfully!")
        return True
        
    except Exception as e:
        print(f"Error registering user: {e}")
        return False