from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from starlette.middleware.base import BaseHTTPMiddleware
import time
import re
from typing import List
import logging

logger = logging.getLogger(__name__)
limiter = Limiter(key_func=get_remote_address)
rate_limit_exceeded_handler = _rate_limit_exceeded_handler
class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        response.headers["Content-Security-Policy"] = "default-src 'self'; script-src 'self' 'unsafe-inline' 'unsafe-eval'; style-src 'self' 'unsafe-inline';"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response.headers["Permissions-Policy"] = "geolocation=(), microphone=(), camera=()"
        return response
class SQLInjectionMiddleware(BaseHTTPMiddleware):
    SQL_PATTERNS = [
        r"(\b(SELECT|INSERT|UPDATE|DELETE|DROP|UNION|ALTER|CREATE|TRUNCATE)\b)",
        r"(--|\bOR\b|\bAND\b)",
        r"('.*\bOR\b.*')",
        r"(\bexec\b|\bxp_\b|\bsp_\b)"
    ]
    async def dispatch(self, request: Request, call_next):
        if request.method in ["POST", "PUT", "PATCH"]:
            body = await request.body()
            if body:
                try:
                    body_str = body.decode()
                    for pattern in self.SQL_PATTERNS:
                        if re.search(pattern, body_str, re.IGNORECASE):
                            logger.warning(f"Potential SQL injection detected from {request.client.host}")
                            raise HTTPException(status_code=400, detail="Invalid request")
                except:
                    pass
        return await call_next(request)
class XSSProtectionMiddleware(BaseHTTPMiddleware):
    XSS_PATTERNS = [
        r"<script",
        r"javascript:",
        r"on\w+=",
        r"&#",
        r"%3Cscript%3E"
    ]
    async def dispatch(self, request: Request, call_next):
        if request.method in ["POST", "PUT", "PATCH"]:
            body = await request.body()
            if body:
                try:
                    body_str = body.decode()
                    for pattern in self.XSS_PATTERNS:
                        if re.search(pattern, body_str, re.IGNORECASE):
                            logger.warning(f"Potential XSS attack detected from {request.client.host}")
                            raise HTTPException(status_code=400, detail="Invalid request")
                except:
                    pass
        return await call_next(request)
class SecurityBearer(HTTPBearer):
    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super().__call__(request)
        if not credentials:
            raise HTTPException(status_code=403, detail="Invalid authentication credentials")
        if not self.verify_token(credentials.credentials):
            raise HTTPException(status_code=403, detail="Invalid token")
        return credentials.credentials
    def verify_token(self, token: str) -> bool:
        return len(token) > 20
class InputValidator:
    @staticmethod
    def validate_email(email: str) -> bool:
        pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        return bool(re.match(pattern, email))
    @staticmethod
    def validate_password(password: str) -> bool:
        if len(password) < 8:
            return False
        if not re.search(r"[A-Z]", password):
            return False
        if not re.search(r"[a-z]", password):
            return False
        if not re.search(r"\d", password):
            return False
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
            return False
        return True
    @staticmethod
    def sanitize_input(input_str: str) -> str:
        return re.sub(r"[<>\"'%();/\\]", "", input_str)