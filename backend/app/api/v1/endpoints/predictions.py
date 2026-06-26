from fastapi import APIRouter, Depends, BackgroundTasks, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.core.database import get_db
from app.schemas.predictions import PredictionRequest, PredictionResponse
from app.services.predictions import PredictionsService

router = APIRouter()

@router.post("/", response_model=PredictionResponse, status_code=status.HTTP_202_ACCEPTED)
async def create_prediction(
    request: PredictionRequest,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db),
):
    service = PredictionsService(db)
    prediction = await service.create_prediction(request)
    
    # Запускаем задачу в фоне
    background_tasks.add_task(service.run_prediction, prediction.id)
    
    return prediction

@router.get("/", response_model=List[PredictionResponse])
async def list_predictions(
    limit: int = 50, 
    offset: int = 0, 
    db: AsyncSession = Depends(get_db)
):
    service = PredictionsService(db)
    return await service.list_predictions(limit, offset)

@router.get("/{prediction_id}", response_model=PredictionResponse)
async def get_prediction(
    prediction_id: int, 
    db: AsyncSession = Depends(get_db)
):
    service = PredictionsService(db)
    prediction = await service.get_prediction(prediction_id)
    if not prediction:
        raise HTTPException(status_code=404, detail="Prediction not found")
    return prediction