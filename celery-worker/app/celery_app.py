import os
from celery import Celery
from celery.schedules import crontab
broker_url = os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/2")
result_backend = os.getenv("CELERY_RESULT_BACKEND", "redis://localhost:6379/3")
celery_app = Celery("foresight", broker=broker_url, backend=result_backend, include=["app.tasks.metrics", "app.tasks.predictions"])
celery_app.conf.update(
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    task_acks_late=True,
    worker_prefetch_multiplier=1,
)
celery_app.conf.beat_schedule = {
    "aggregate-metrics-every-minute": {
        "task": "app.tasks.metrics.aggregate_metrics",
        "schedule": crontab(minute="*"),
    },
    "cleanup-old-predictions-daily": {
        "task": "app.tasks.predictions.cleanup_old_predictions",
        "schedule": crontab(hour=2, minute=0),
    },
}
