from utils import generate_checksum, generate_random_code
from database import get_activation_code, increment_code_usage
import logging

logger = logging.getLogger(__name__)

async def generate_activation_code(length: int = 16, prefix: str = "", suffix: str = "", with_checksum: bool = True) -> str:
    while True:
        full_code = generate_random_code(length, prefix, suffix, with_checksum)
        if not await get_activation_code(full_code):
            return full_code

async def validate_activation_code(activation_code: str, app_id: str) -> bool:
    logger.debug(f"Validating code: {activation_code} for app_id: {app_id}")
    code_parts = activation_code.rsplit('-', 1)
    
    if len(code_parts) == 2:
        code, checksum = code_parts
        logger.debug(f"Code: {code}, Checksum: {checksum}")
        if generate_checksum(code) != checksum:
            logger.debug("Checksum validation failed")
            return False
    else:
        code = activation_code
        logger.debug("No checksum found in the activation code")

    stored_code = await get_activation_code(activation_code)  # Use full activation_code here
    logger.debug(f"Stored code: {stored_code}")
    if stored_code and stored_code['app_id'] == app_id:
        await increment_code_usage(activation_code)  # Use full activation_code here
        logger.debug("Code is valid and usage incremented")
        return True
    logger.debug("Code is invalid or app_id doesn't match")
    return False
