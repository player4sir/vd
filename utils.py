import random
import string
import hashlib
from typing import Optional

def generate_checksum(code: str) -> str:
    """Generate a 4-character checksum for the given code."""
    if not code:
        raise ValueError("Code cannot be empty")
    return hashlib.md5(code.encode()).hexdigest()[:4]

def generate_random_code(
    length: int = 16,
    prefix: str = "",
    suffix: str = "",
    with_checksum: bool = True,
    characters: Optional[str] = None
) -> str:
    """Generate a random code with optional prefix, suffix, and checksum."""
    if length < 1:
        raise ValueError("Length must be at least 1")
    
    if characters is None:
        characters = string.ascii_uppercase + string.digits
    
    # Use secrets module for cryptographically strong random choices
    import secrets
    main_code = ''.join(secrets.choice(characters) for _ in range(length))
    full_code = f"{prefix}{main_code}{suffix}"
    
    if with_checksum:
        checksum = generate_checksum(full_code)
        full_code = f"{full_code}-{checksum}"
    
    return full_code

def validate_checksum(code: str) -> bool:
    """Validate the checksum of a given code."""
    if not code or '-' not in code:
        return False
    
    main_code, checksum = code.rsplit('-', 1)
    return generate_checksum(main_code) == checksum
