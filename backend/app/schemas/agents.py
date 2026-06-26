import enum
from datetime import datetime
from typing import Any

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
    config: dict[str, Any] | None = None  # ← Dict → dict


class AgentUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    status: AgentStatus | None = None
    config: dict[str, Any] | None = None  # ← Dict → dict


class AgentResponse(BaseModel):
    id: int
    name: str
    type: str
    description: str | None = None
    status: AgentStatus
    config: dict[str, Any] | None = None  # ← Dict → dict
    last_seen: datetime | None = None
    created_at: datetime

    class Config:
        from_attributes = True