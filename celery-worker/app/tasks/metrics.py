import structlog
from app.celery_app import celery_app
log = structlog.get_logger()
@celery_app.task(bind=True, max_retries=3)
def aggregate_metrics(self):
    try:
        log.info("aggregating metrics")
        return {"status": "ok", "aggregated": 0}
    except Exception as exc:
        log.error("failed to aggregate metrics", error=str(exc))
        raise self.retry(exc=exc, countdown=60)
@celery_app.task(bind=True, max_retries=3)
def process_metric_batch(self, metrics: list):
    try:
        log.info("processing metric batch", count=len(metrics))
        return {"status": "ok", "processed": len(metrics)}
    except Exception as exc:
        log.error("failed to process metric batch", error=str(exc))
        raise self.retry(exc=exc, countdown=30)
