from unittest.mock import patch
from app.tasks.metrics import aggregate_metrics, process_metric_batch
from app.tasks.predictions import run_prediction, cleanup_old_predictions
def test_aggregate_metrics_task_exists():
    assert aggregate_metrics is not None
def test_process_metric_batch_task_exists():
    assert process_metric_batch is not None
def test_run_prediction_task_exists():
    assert run_prediction is not None
def test_cleanup_old_predictions_task_exists():
    assert cleanup_old_predictions is not None
