from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime
from typing import Optional, List
from app.schemas.metrics import MetricCreate, MetricResponse
class MetricsService:
    def __init__(self, db: AsyncSession):
        self.db = db
    async def list_metrics(self, agent_id, metric_type, from_dt, to_dt, limit, offset) -> List[MetricResponse]:
        return []
    async def create_metric(self, data: MetricCreate) -> MetricResponse:
        return MetricResponse(id=1, agent_id=data.agent_id, metric_type=data.metric_type, value=data.value, metadata=data.metadata, timestamp=datetime.utcnow())
    async def get_metric(self, metric_id: int) -> Optional[MetricResponse]:
        return None
    async def get_summary(self) -> dict:
        return {"total": 0, "agents": 0, "metric_types": []}
