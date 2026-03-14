# Timer Job

## Overview

This recipe demonstrates scheduled execution using Azure Functions timer
triggers and NCRONTAB expressions. It is a clean pattern for recurring
maintenance, reconciliation, and periodic automation.

The paired runnable project is `examples/timer_job`.

## Primary use case

Use this pattern when you need:

- periodic tasks without external event producers
- deterministic schedule execution
- catch-up behavior awareness (`past_due`)
- lightweight maintenance workflows

## Architecture diagram (text)

```text
NCRONTAB schedule (0 */5 * * * *)
  |
  v
Azure Functions Runtime scheduler
  |
  | timer trigger
  v
scheduled_job(timer)
  |- check timer.past_due
  |- log execution timestamp
  '- execute maintenance task
```

## Prerequisites

- Python 3.10+
- Azure Functions Core Tools v4
- `azure-functions`

Install and run:

```bash
cd examples/timer_job
pip install -r requirements.txt
func start
```

## Step-by-step implementation guide

Implementation flow in `examples/timer_job/function_app.py`:

1. Define `app = func.FunctionApp()` and logger.
2. Add maintenance function `_perform_maintenance()`.
3. Register timer trigger with `schedule="0 */5 * * * *"`.
4. Compute UTC timestamp at trigger time.
5. Check `timer.past_due` and log warning when needed.
6. Execute maintenance function and log completion.

## Complete code walkthrough

### App and maintenance function

```python
import azure.functions as func
import datetime
import logging

app = func.FunctionApp()
logger = logging.getLogger(__name__)

def _perform_maintenance() -> str:
    logger.info("Running scheduled maintenance")
    return "maintenance complete"
```

The maintenance function is intentionally small so scheduling behavior remains
the focus.

### Timer trigger registration and handler

```python
@app.timer_trigger(
    schedule="0 */5 * * * *",
    arg_name="timer",
    run_on_startup=False,
    use_monitor=True,
)
def scheduled_job(timer: func.TimerRequest) -> None:
    utc_now = datetime.datetime.now(tz=datetime.timezone.utc).isoformat()

    if timer.past_due:
        logger.warning("Timer is past due — running catch-up execution at %s", utc_now)

    logger.info("Timer trigger fired at %s", utc_now)
    result = _perform_maintenance()
    logger.info("Scheduled job finished: %s", result)
```

Key options:

- `run_on_startup=False`: avoid automatic run during startup
- `use_monitor=True`: runtime tracks schedule state across restarts

## NCRONTAB reference

Azure Functions uses a six-field format:

```text
{second} {minute} {hour} {day} {month} {day-of-week}
```

Common examples from source recipe guidance:

- `0 */5 * * * *` -> every 5 minutes
- `0 0 * * * *` -> top of every hour
- `0 0 0 * * *` -> midnight every day
- `0 0 0 * * 1-5` -> midnight on weekdays

## Running locally

```bash
cd examples/timer_job
pip install -r requirements.txt
func start
```

You can wait for schedule execution, or trigger manually:

```bash
curl -X POST http://localhost:7071/admin/functions/scheduled_job -H "Content-Type: application/json" -d '{"input":"test"}'
```

## Expected output

Typical log sequence:

```text
Timer trigger fired at 2026-03-14T08:10:00.000000+00:00
Running scheduled maintenance
Scheduled job finished: maintenance complete
```

Catch-up path example:

```text
Timer is past due — running catch-up execution at 2026-03-14T08:15:00.000000+00:00
```

## Production considerations

- Keep timer handlers idempotent (at-least-once execution semantics).
- Keep schedule in UTC unless explicit timezone requirements exist.
- Set `WEBSITE_TIME_ZONE` only when local-time scheduling is required.
- Keep tasks short, or offload orchestration for long-running jobs.
- Monitor duration and failure rates in Application Insights.
- Avoid overlapping schedules that overload shared dependencies.
- Keep external calls resilient with timeout/retry policies.
- Use managed identity for secure Azure resource access.

!!! warning
    Timer triggers are not a replacement for event-driven architecture.
    Use queue or webhook triggers when events already exist.

## Additional testing notes

The source recipe recommends testing business logic separately from trigger
wiring. Keep core task functions unit-testable and independent from timer I/O.

## Related recipes

- For async work kicked off by external producers, see [Queue Worker](queue-worker.md).
- For request/response API operations, see [HTTP API Basic](http-api-basic.md).

## Ecosystem links

- `azure-functions-logging` for run telemetry and diagnostics
- `azure-functions-doctor` for environment diagnosis
- `azure-functions-scaffold` for starter generation
