from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from activation_code import generate_activation_code, validate_activation_code
from database import init_db, save_activation_code, revoke_activation_code, bulk_generate_codes
from datetime import datetime, timedelta, UTC
from typing import List, Optional
import time
from fastapi.security import APIKeyHeader
import os
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # 启动时运行
    await init_db()
    yield
    # 关闭时运行
    # 如果需要在应用关闭时执行清理操作，可以在这里添加

app = FastAPI(lifespan=lifespan)

# 添加CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有来源，您可以根据需要限制
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 简单的速率限制


class RateLimiter:
    def __init__(self, calls: int, period: int):
        self.calls = calls
        self.period = period
        self.timestamps = []

    def is_allowed(self):
        now = time.time()
        self.timestamps = [t for t in self.timestamps if now - t < self.period]
        if len(self.timestamps) < self.calls:
            self.timestamps.append(now)
            return True
        return False


rate_limiter = RateLimiter(calls=10, period=60)  # 每分钟10次请求

# 简单的API密钥验证
API_KEY = os.getenv("API_KEY")
api_key_header = APIKeyHeader(name="X-API-Key")


def verify_api_key(api_key: str = Depends(api_key_header)):
    if api_key != API_KEY:
        raise HTTPException(status_code=403, detail="Invalid API Key")


class ActivationCodeRequest(BaseModel):
    app_id: str
    length: int = 16
    prefix: str = ""
    suffix: str = ""
    with_checksum: bool = True
    expires_in_days: Optional[int] = None
    max_uses: Optional[int] = None


class ActivationCodeResponse(BaseModel):
    activation_code: str


class ValidateRequest(BaseModel):
    activation_code: str
    app_id: str



class BulkGenerateRequest(BaseModel):
    app_id: str
    count: int
    expires_in_days: Optional[int] = None
    max_uses: Optional[int] = None


class RevokeRequest(BaseModel):
    activation_code: str


@app.post("/generate", response_model=ActivationCodeResponse, dependencies=[Depends(verify_api_key)])
async def generate_code(request: ActivationCodeRequest):
    if not rate_limiter.is_allowed():
        raise HTTPException(status_code=429, detail="Rate limit exceeded")

    activation_code = await generate_activation_code(
        length=request.length,
        prefix=request.prefix,
        suffix=request.suffix,
        with_checksum=request.with_checksum
    )
    expires_at = datetime.now(UTC) + \
        timedelta(days=request.expires_in_days) if request.expires_in_days else None
    await save_activation_code(activation_code, request.app_id, expires_at, request.max_uses)
    return ActivationCodeResponse(activation_code=activation_code)


@app.post("/validate")
async def validate_code(request: ValidateRequest):
    if not rate_limiter.is_allowed():
        raise HTTPException(status_code=429, detail="Rate limit exceeded")
    
    logger.debug(f"Validating code: {request.activation_code} for app_id: {request.app_id}")
    is_valid = await validate_activation_code(request.activation_code, request.app_id)
    logger.debug(f"Validation result: {is_valid}")
    if is_valid:
        return {"valid": True, "message": "Activation code is valid"}
    else:
        raise HTTPException(status_code=400, detail="Invalid activation code")


@app.post("/bulk_generate", response_model=List[str], dependencies=[Depends(verify_api_key)])
async def bulk_generate(request: BulkGenerateRequest):
    if not rate_limiter.is_allowed():
        raise HTTPException(status_code=429, detail="Rate limit exceeded")

    expires_at = datetime.now(datetime.UTC) + \
        timedelta(days=request.expires_in_days) if request.expires_in_days else None
    codes = await bulk_generate_codes(request.app_id, request.count, expires_at, request.max_uses)
    return codes


@app.post("/revoke", dependencies=[Depends(verify_api_key)])
async def revoke_code(request: RevokeRequest):
    if not rate_limiter.is_allowed():
        raise HTTPException(status_code=429, detail="Rate limit exceeded")

    await revoke_activation_code(request.activation_code)
    return {"message": "Activation code revoked successfully"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
