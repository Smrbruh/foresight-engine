from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from datetime import datetime
from app.core.database import get_db
from app.schemas.metrics import MetricResponse, MetricCreate
from app.services.metrics import MetricsService
router = APIRouter()
@router.get("/", response_model=List[MetricResponse])
async def list_metrics(
    agent_id: Optional[int] = None,
    metric_type: Optional[str] = None,
    from_dt: Optional[datetime] = Query(None),
    to_dt: Optional[datetime] = Query(None),
    limit: int = Query(100, le=1000),
    offset: int = 0,
    db: AsyncSession = Depends(get_db),
):
    service = MetricsService(db)
    return await service.list_metrics(agent_id, metric_type, from_dt, to_dt, limit, offset)
@router.post("/", response_model=MetricResponse, status_code=201)
async def create_metric(data: MetricCreate, db: AsyncSession = Depends(get_db)):
    service = MetricsService(db)
    return await service.create_metric(data)
@router.get("/summary")
async def metrics_summary(db: AsyncSession = Depends(get_db)):
    service = MetricsService(db)
    return await service.get_summary()
@router.get("/{metric_id}", response_model=MetricResponse)
async def get_metric(metric_id: int, db: AsyncSession = Depends(get_db)):
    service = MetricsService(db)
    return await service.get_metric(metric_id)
