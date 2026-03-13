"""Timer-triggered scheduled job."""

from __future__ import annotations

import datetime
import logging

import azure.functions as func

app = func.FunctionApp()

logger = logging.getLogger(__name__)


def _perform_maintenance() -> str:
    """Simulate a periodic maintenance task."""
    logger.info("Running scheduled maintenance")
    return "maintenance complete"


@app.timer_trigger(
    schedule="0 */5 * * * *",
    arg_name="timer",
    run_on_startup=False,
    use_monitor=True,
)
def scheduled_job(timer: func.TimerRequest) -> None:
    """Run every 5 minutes to perform periodic maintenance."""
    utc_now = datetime.datetime.now(tz=datetime.timezone.utc).isoformat()

    if timer.past_due:
        logger.warning("Timer is past due — running catch-up execution at %s", utc_now)

    logger.info("Timer trigger fired at %s", utc_now)
    result = _perform_maintenance()
    logger.info("Scheduled job finished: %s", result)
