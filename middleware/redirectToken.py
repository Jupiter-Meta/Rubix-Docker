import hashlib
import base64
import os


def generate_token(userID, DID):
    # Step 1: Concatenate userID and DID
    combined_string = userID + DID + os.urandom(16).hex()
    
    # Step 2: Hash the concatenated string using SHA-256
    sha256_hash = hashlib.sha256(combined_string.encode()).digest()
    
    # Step 3: Encode the hash in base64 to ensure it is 256 characters
    base64_encoded_hash = base64.b64encode(sha256_hash).decode()
    
    # Step 4: Ensure the final token is 256 characters by padding or truncating
    # Repeat the base64_encoded_hash to ensure we have enough characters
    while len(base64_encoded_hash) < 256:
        base64_encoded_hash += base64.b64encode(hashlib.sha256(base64_encoded_hash.encode()).digest()).decode()
    
    # Truncate to 256 characters if necessary
    final_token = base64_encoded_hash[:256]
    
    return final_token