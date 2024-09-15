import random
import string
import hashlib

def generate_checksum(code: str) -> str:
    return hashlib.md5(code.encode()).hexdigest()[:4]

def generate_random_code(length: int = 16, prefix: str = "", suffix: str = "", with_checksum: bool = True) -> str:
    characters = string.ascii_uppercase + string.digits
    main_code = ''.join(random.choice(characters) for _ in range(length))
    full_code = f"{prefix}{main_code}{suffix}"
    
    if with_checksum:
        checksum = generate_checksum(full_code)
        full_code = f"{full_code}-{checksum}"
    
    return full_code
