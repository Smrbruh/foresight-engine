import enum
from datetime import datetime
from typing import Any, Dict

from pydantic import BaseModel


class AgentStatus(enum.StrEnum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    ERROR = "error"


class AgentCreate(BaseModel):
    name: str
    type: str
    description: str | None = None
    status: AgentStatus = AgentStatus.ACTIVE
    config: Dict[str, Any] | None = None


class AgentUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    status: AgentStatus | None = None
    config: Dict[str, Any] | None = None


class AgentResponse(BaseModel):
    id: int
    name: str
    type: str
    description: str | None = None
    status: AgentStatus
    config: Dict[str, Any] | None = None
    last_seen: datetime | None = None
    created_at: datetime

    class Config:
        from_attributes = True