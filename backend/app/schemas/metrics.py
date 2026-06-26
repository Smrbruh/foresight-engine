from datetime import datetime
from typing import Any

from pydantic import BaseModel


class MetricCreate(BaseModel):
    agent_id: int
    metric_type: str
    value: float
    metadata: dict[str, Any] | None = None
    timestamp: datetime | None = None


class MetricResponse(BaseModel):
    id: int
    agent_id: int
    metric_type: str
    value: float
    metadata: dict[str, Any] | None = None
    timestamp: datetime

    class Config:
        from_attributes = True