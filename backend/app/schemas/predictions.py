import enum
from datetime import datetime
from typing import Any, Dict

from pydantic import BaseModel


class PredictionStatus(enum.StrEnum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


class PredictionRequest(BaseModel):
    agent_id: int
    model_type: str
    horizon_hours: int = 24
    parameters: Dict[str, Any] | None = None


class PredictionResponse(BaseModel):
    id: int
    agent_id: int
    model_type: str
    horizon_hours: int
    status: PredictionStatus
    result: Dict[str, Any] | None = None
    created_at: datetime
    completed_at: datetime | None = None

    class Config:
        from_attributes = True