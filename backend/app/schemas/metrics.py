from pydantic import BaseModel
from datetime import datetime
from typing import Optional, Dict, Any
class MetricCreate(BaseModel):
    agent_id: int
    metric_type: str
    value: float
    metadata: Optional[Dict[str, Any]] = None
    timestamp: Optional[datetime] = None
class MetricResponse(BaseModel):
    id: int
    agent_id: int
    metric_type: str
    value: float
    metadata: Optional[Dict[str, Any]] = None
    timestamp: datetime
    class Config:
        from_attributes = True
