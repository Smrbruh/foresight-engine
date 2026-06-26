from pydantic import BaseModel
from datetime import datetime
from typing import Optional, Dict, Any
from enum import Enum
class PredictionStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
class PredictionRequest(BaseModel):
    agent_id: int
    model_type: str
    horizon_hours: int = 24
    parameters: Optional[Dict[str, Any]] = None
class PredictionResponse(BaseModel):
    id: int
    agent_id: int
    model_type: str
    horizon_hours: int
    status: PredictionStatus
    result: Optional[Dict[str, Any]] = None
    created_at: datetime
    completed_at: Optional[datetime] = None
    class Config:
        from_attributes = True
