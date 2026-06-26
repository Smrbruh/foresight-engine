from sqlalchemy import Column, Integer, String, DateTime, JSON, Enum
from sqlalchemy.sql import func
from app.core.database import Base
from app.core.encryption import encryption
import enum
import json

class AgentStatus(enum.StrEnum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    ERROR = "error"

class Agent(Base):
    __tablename__ = "agents"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    type = Column(String, nullable=False)
    description = Column(String, nullable=True)
    status = Column(Enum(AgentStatus), default=AgentStatus.ACTIVE)
    _config = Column("config", JSON, default={})
    last_seen = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    @property
    def config(self):
        """Возвращает расшифрованный конфиг"""
        if self._config:
            return json.loads(encryption.decrypt(json.dumps(self._config)))
        return {}
    
    @config.setter
    def config(self, value):
        """Шифрует конфиг перед сохранением"""
        if value:
            self._config = json.loads(encryption.encrypt(json.dumps(value)))
        else:
            self._config = {}