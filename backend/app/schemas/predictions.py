import enum
from datetime import datetime
from typing import Any

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
    parameters: dict[str, Any] | None = None  # ← Dict → dict


class PredictionResponse(BaseModel):
    id: int
    agent_id: int
    model_type: str
    horizon_hours: int
    status: PredictionStatus
    result: dict[str, Any] | None = None  # ← Dict → dict
    created_at: datetime
    completed_at: datetime | None = None

    class Config:
        from_attributes = True
