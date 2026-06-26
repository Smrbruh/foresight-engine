from datetime import UTC, datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.prediction import Prediction
from app.schemas.predictions import PredictionRequest, PredictionResponse, PredictionStatus


class PredictionsService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_prediction(self, request: PredictionRequest) -> PredictionResponse:
        prediction = Prediction(
            agent_id=request.agent_id,
            model_type=request.model_type,
            horizon_hours=request.horizon_hours or 24,
            status=PredictionStatus.PENDING,
            parameters=request.parameters or {},
            created_at=datetime.now(UTC),
        )
        self.db.add(prediction)
        await self.db.commit()
        await self.db.refresh(prediction)

        return PredictionResponse(
            id=prediction.id,
            agent_id=prediction.agent_id,
            model_type=prediction.model_type,
            horizon_hours=prediction.horizon_hours,
            status=prediction.status,
            result=prediction.result,
            created_at=prediction.created_at,
            completed_at=prediction.completed_at,
        )

    async def run_prediction(self, prediction_id: int):
        prediction = await self.get_prediction(prediction_id)
        if prediction:
            prediction.status = PredictionStatus.PROCESSING
            await self.db.commit()

            import asyncio

            await asyncio.sleep(2)

            prediction.status = PredictionStatus.COMPLETED
            prediction.result = {"forecast": [], "confidence": 0.95}
            prediction.completed_at = datetime.now(UTC)
            await self.db.commit()

    async def list_predictions(self, limit: int, offset: int) -> list[PredictionResponse]:
        stmt = select(Prediction).limit(limit).offset(offset).order_by(Prediction.created_at.desc())
        result = await self.db.execute(stmt)
        predictions = result.scalars().all()

        return [
            PredictionResponse(
                id=p.id,
                agent_id=p.agent_id,
                model_type=p.model_type,
                horizon_hours=p.horizon_hours,
                status=p.status,
                result=p.result,
                created_at=p.created_at,
                completed_at=p.completed_at,
            )
            for p in predictions
        ]

    async def get_prediction(self, prediction_id: int) -> PredictionResponse | None:
        stmt = select(Prediction).where(Prediction.id == prediction_id)
        result = await self.db.execute(stmt)
        prediction = result.scalar_one_or_none()

        if not prediction:
            return None

        return PredictionResponse(
            id=prediction.id,
            agent_id=prediction.agent_id,
            model_type=prediction.model_type,
            horizon_hours=prediction.horizon_hours,
            status=prediction.status,
            result=prediction.result,
            created_at=prediction.created_at,
            completed_at=prediction.completed_at,
        )
