import os
import asyncpg
from dotenv import load_dotenv
from datetime import datetime
import logging

logger = logging.getLogger(__name__)
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

async def get_connection():
    return await asyncpg.create_pool(DATABASE_URL)

async def init_db():
    pool = await get_connection()
    async with pool.acquire() as conn:
        await conn.execute('''
            CREATE TABLE IF NOT EXISTS activation_codes (
                code TEXT PRIMARY KEY,
                app_id TEXT,
                created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
                expires_at TIMESTAMP WITH TIME ZONE,
                max_uses INTEGER,
                current_uses INTEGER DEFAULT 0,
                is_revoked BOOLEAN DEFAULT FALSE
            )
        ''')

async def save_activation_code(code: str, app_id: str = None, expires_at: datetime = None, max_uses: int = None):
    pool = await get_connection()
    async with pool.acquire() as conn:
        await conn.execute(
            '''
            INSERT INTO activation_codes (code, app_id, expires_at, max_uses)
            VALUES ($1, $2, $3, $4)
            ''',
            code, app_id, expires_at, max_uses
        )

async def get_activation_code(code: str):
    logger.debug(f"Fetching activation code: {code}")
    pool = await get_connection()
    async with pool.acquire() as conn:
        result = await conn.fetchrow(
            '''
            SELECT * FROM activation_codes
            WHERE code = $1 AND (expires_at IS NULL OR expires_at > CURRENT_TIMESTAMP)
            AND (max_uses IS NULL OR current_uses < max_uses)
            AND NOT is_revoked
            ''',
            code
        )
    logger.debug(f"Fetch result: {result}")
    return result

async def increment_code_usage(code: str):
    pool = await get_connection()
    async with pool.acquire() as conn:
        await conn.execute(
            '''
            UPDATE activation_codes
            SET current_uses = current_uses + 1
            WHERE code = $1
            ''',
            code
        )

async def revoke_activation_code(code: str):
    pool = await get_connection()
    async with pool.acquire() as conn:
        await conn.execute(
            '''
            UPDATE activation_codes
            SET is_revoked = TRUE
            WHERE code = $1
            ''',
            code
        )

async def update_activation_code(code: str, app_id: str):
    pool = await get_connection()
    async with pool.acquire() as conn:
        result = await conn.execute(
            '''
            UPDATE activation_codes
            SET app_id = $2
            WHERE code = $1 AND app_id IS NULL
            ''',
            code, app_id
        )
    return result != "UPDATE 0"

async def bulk_generate_codes(app_id: str, count: int, expires_at: datetime = None, max_uses: int = None):
    from activation_code import generate_activation_code
    codes = [await generate_activation_code() for _ in range(count)]
    pool = await get_connection()
    async with pool.acquire() as conn:
        await conn.executemany(
            '''
            INSERT INTO activation_codes (code, app_id, expires_at, max_uses)
            VALUES ($1, $2, $3, $4)
            ''',
            [(code, app_id, expires_at, max_uses) for code in codes]
        )
    return codes

async def get_activation_codes(limit: int = 100, offset: int = 0):
    pool = await get_connection()
    async with pool.acquire() as conn:
        results = await conn.fetch(
            '''
            SELECT code, app_id, created_at, expires_at, max_uses, current_uses, is_revoked
            FROM activation_codes
            ORDER BY created_at DESC
            LIMIT $1 OFFSET $2
            ''',
            limit, offset
        )
    return [dict(result) for result in results]

async def get_app_activation_code(app_id: str):
    pool = await get_connection()
    async with pool.acquire() as conn:
        return await conn.fetchrow(
            '''
            SELECT * FROM activation_codes
            WHERE app_id = $1
            ''',
            app_id
        )