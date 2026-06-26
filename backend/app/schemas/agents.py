from pydantic import BaseModel
from datetime import datetime
from typing import Optional, Dict, Any
from enum import Enum

class AgentStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    ERROR = "error"

class AgentCreate(BaseModel):
    name: str
    type: str
    description: Optional[str] = None
    status: AgentStatus = AgentStatus.ACTIVE
    config: Optional[Dict[str, Any]] = None

class AgentUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    status: Optional[AgentStatus] = None
    config: Optional[Dict[str, Any]] = None

class AgentResponse(BaseModel):
    id: int
    name: str
    type: str
    description: Optional[str] = None
    status: AgentStatus
    config: Optional[Dict[str, Any]] = None
    last_seen: Optional[datetime] = None
    created_at: datetime

    class Config:
        from_attributes = True