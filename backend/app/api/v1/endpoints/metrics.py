from datetime import datetime

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.schemas.metrics import MetricCreate, MetricResponse
from app.services.metrics import MetricsService

router = APIRouter()


@router.get("/", response_model=list[MetricResponse])
async def list_metrics(
    agent_id: int | None = None,
    metric_type: str | None = None,
    from_dt: datetime | None = Query(None),
    to_dt: datetime | None = Query(None),
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
