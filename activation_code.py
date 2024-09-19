from datetime import UTC, datetime
from utils import generate_checksum, generate_random_code
from database import get_activation_code, increment_code_usage, save_activation_code, update_activation_code, get_app_activation_code
import logging

logger = logging.getLogger(__name__)

async def generate_activation_code(length: int = 16, prefix: str = "", suffix: str = "", with_checksum: bool = True) -> str:
    while True:
        full_code = generate_random_code(length, prefix, suffix, with_checksum)
        if not await get_activation_code(full_code):
            await save_activation_code(full_code)
            return full_code

async def bind_activation_code(activation_code: str, app_id: str) -> dict:
    # 检查激活码是否存在
    stored_code = await get_activation_code(activation_code)
    if not stored_code:
        logger.debug(f"Activation code {activation_code} does not exist")
        return {"success": False, "message": "Activation code does not exist"}

    # 检查激活码是否已被使用
    if stored_code['app_id'] is not None:
        logger.debug(f"Activation code {activation_code} has already been used")
        return {"success": False, "message": "Activation code has already been used"}

    # 检查 app_id 是否已经绑定了其他激活码
    existing_app_code = await get_app_activation_code(app_id)
    if existing_app_code:
        logger.debug(f"App ID {app_id} is already bound to another activation code")
        return {"success": False, "message": "App ID is already bound to another activation code"}

    # 检查激活码是否过期
    if stored_code['expires_at'] and stored_code['expires_at'] < datetime.now(UTC):
        logger.debug(f"Activation code {activation_code} has expired")
        return {"success": False, "message": "Activation code has expired"}

    # 检查激活码是否超过最大使用次数
    if stored_code['max_uses'] and stored_code['current_uses'] >= stored_code['max_uses']:
        logger.debug(f"Activation code {activation_code} has reached maximum uses")
        return {"success": False, "message": "Activation code has reached maximum uses"}

    # 绑定激活码
    success = await update_activation_code(activation_code, app_id)
    if success:
        logger.debug(f"Activation code {activation_code} bound to app_id {app_id}")
        return {"success": True, "message": "Activation successful"}
    else:
        logger.debug(f"Failed to bind activation code {activation_code} to app_id {app_id}")
        return {"success": False, "message": "Failed to bind activation code"}

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

    stored_code = await get_activation_code(activation_code)
    logger.debug(f"Stored code: {stored_code}")
    if stored_code and stored_code['app_id'] == app_id:
        # 检查是否过期
        if stored_code['expires_at'] and stored_code['expires_at'] < datetime.now(UTC):
            logger.debug("Code has expired")
            return False
        # 检查是否超过最大使用次数
        if stored_code['max_uses'] and stored_code['current_uses'] >= stored_code['max_uses']:
            logger.debug("Code has reached maximum uses")
            return False
        await increment_code_usage(activation_code)
        logger.debug("Code is valid and usage incremented")
        return True
    logger.debug("Code is invalid or app_id doesn't match")
    return False

async def unbind_activation_code(app_id: str) -> dict:
    success = await unbind_activation_code(app_id)
    if success:
        logger.debug(f"Activation code unbound from app_id {app_id}")
        return {"success": True, "message": "Activation code unbound successfully"}
    else:
        logger.debug(f"Failed to unbind activation code for app_id {app_id}")
        return {"success": False, "message": "Failed to unbind activation code"}

async def delete_activation_code(code: str) -> dict:
    success = await delete_activation_code(code)
    if success:
        logger.debug(f"Activation code {code} deleted")
        return {"success": True, "message": "Activation code deleted successfully"}
    else:
        logger.debug(f"Failed to delete activation code {code}")
        return {"success": False, "message": "Failed to delete activation code"}