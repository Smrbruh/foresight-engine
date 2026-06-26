import pytest
from app.tasks.metrics import aggregate_metrics, process_metric_batch
from app.tasks.predictions import run_prediction, cleanup_old_predictions


@pytest.mark.asyncio
async def test_aggregate_metrics():
    result = aggregate_metrics()
    assert result["status"] == "ok"


@pytest.mark.asyncio
async def test_process_metric_batch():
    result = process_metric_batch()
    assert result["status"] == "ok"


@pytest.mark.asyncio
async def test_run_prediction():
    result = run_prediction(1, "test", {})
    assert result["status"] == "completed"


@pytest.mark.asyncio
async def test_cleanup_old_predictions():
    result = cleanup_old_predictions()
    assert result["deleted"] == 0