import enum

from sqlalchemy import JSON, Column, DateTime, Enum, Integer, String
from sqlalchemy.sql import func

from app.core.database import Base


class AgentStatus(enum.StrEnum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    ERROR = "error"


class Agent(Base):
    __tablename__ = "agents"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    type = Column(String, nullable=False)  # ← Добавляем поле type
    description = Column(String, nullable=True)
    status = Column(Enum(AgentStatus), default=AgentStatus.ACTIVE)
    config = Column(JSON, default={})
    last_seen = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
