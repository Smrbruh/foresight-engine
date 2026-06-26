import structlog

from app.celery_app import celery_app

log = structlog.get_logger()


@celery_app.task(bind=True, max_retries=2, time_limit=300)
def run_prediction(self, prediction_id: int, model_type: str, parameters: dict):
    try:
        log.info("running prediction", prediction_id=prediction_id, model_type=model_type)
        result = {"forecast": [], "confidence": 0.95, "model": model_type}
        return {"status": "completed", "prediction_id": prediction_id, "result": result}
    except Exception as exc:
        log.error("prediction failed", prediction_id=prediction_id, error=str(exc))
        raise self.retry(exc=exc, countdown=120)


@celery_app.task
def cleanup_old_predictions():
    log.info("cleaning up old predictions")
    return {"deleted": 0}
