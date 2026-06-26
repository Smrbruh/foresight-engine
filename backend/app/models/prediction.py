from sqlalchemy import Column, Integer, String, DateTime, JSON, Enum
from sqlalchemy.sql import func
from app.core.database import Base
import enum

class PredictionStatus(str, enum.Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"

class Prediction(Base):
    __tablename__ = "predictions"
    
    id = Column(Integer, primary_key=True, index=True)
    agent_id = Column(Integer, nullable=False)
    model_type = Column(String, nullable=False)
    horizon_hours = Column(Integer, default=24)
    status = Column(Enum(PredictionStatus), default=PredictionStatus.PENDING)
    parameters = Column(JSON, default={})
    result = Column(JSON, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    completed_at = Column(DateTime(timezone=True), nullable=True)