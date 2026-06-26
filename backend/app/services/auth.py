from datetime import datetime, timedelta

from jose import jwt
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.schemas.auth import UserCreate

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AuthService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_user(self, data: UserCreate):
        # Хэшируем пароль (временно убрали сохранение)
        # hashed_password = pwd_context.hash(data.password)  # закомментировано
        # TODO: Сохранить пользователя в БД с hashed_password
        return {"id": 1, "username": data.username, "email": data.email}

    async def authenticate_user(self, username: str, password: str):
        return type("User", (), {"id": 1, "username": username})()

    def create_access_token(self, data: dict) -> str:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode = {**data, "exp": expire}
        return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)