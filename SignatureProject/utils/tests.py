import sys
import os
from pathlib import Path

# Add the parent directory to sys.path to allow imports
current_dir = Path(__file__).resolve().parent
project_root = current_dir.parent
sys.path.append(str(project_root))

# Now we can import our modules
from utils.rsa.generate import generate_keys
from utils.rsa.save import save_keys

# Create your tests here.
def test_generate_keys():
    private, public = generate_keys()
    save_keys(private, public, "user_1")

if __name__ == "__main__":
    test_generate_keys()
    print("Keys generated and saved successfully!")