# Timer Scheduled Job

## Overview
A time-triggered function that runs on a configurable schedule using CRON expressions. This recipe demonstrates how to build periodic tasks such as data cleanup, report generation, health checks, or synchronization jobs. The function executes automatically at the specified intervals without any external trigger.

## When to Use
- Running periodic maintenance tasks (cache cleanup, log rotation)
- Generating scheduled reports or aggregations
- Polling external systems on a fixed interval
- Health check or heartbeat monitoring
- Scheduled data synchronization between systems

## Architecture
- Azure Functions runtime evaluates the CRON schedule
- At the scheduled time, the timer trigger fires the function
- Function executes its task and returns
- Runtime records execution status and timestamp
- If the function was missed (e.g., during deployment), it can optionally run the missed execution

ASCII diagram:
```text
CRON Schedule -> Azure Functions Runtime -> Timer Function -> Task Execution
                                               |
                                    Timer Status Record (last run)
```

## Project Structure
```text
timer-job/
  function_app.py       # Timer-triggered function
  host.json
  local.settings.json
  requirements.txt
  tests/
    test_timer.py
```

## Implementation

### Python Code Example
The following code demonstrates a Python v2 model function that runs every 5 minutes using an NCRONTAB expression.

```python
import datetime
import logging
import azure.functions as func

app = func.FunctionApp()

@app.timer_trigger(schedule="0 */5 * * * *", 
                  arg_name="myTimer", 
                  run_on_startup=False,
                  use_monitor=True) 
def timer_trigger_function(myTimer: func.TimerRequest) -> None:
    utc_timestamp = datetime.datetime.utcnow().replace(
        tzinfo=datetime.timezone.utc).isoformat()

    if myTimer.past_due:
        logging.info('The timer is past due!')

    logging.info('Python timer trigger function ran at %s', utc_timestamp)
    
    # Place your scheduled logic here
    # Example: run_data_cleanup() or generate_daily_report()
    perform_maintenance_task()

def perform_maintenance_task():
    # Business logic for the scheduled task
    pass
```

### NCRONTAB Expressions
Azure Functions uses the NCronTab library, which supports six fields: `{second} {minute} {hour} {day} {month} {day-of-week}`.

Common examples:
- `0 */5 * * * *`: Every 5 minutes
- `0 0 * * * *`: Every hour at the top of the hour
- `0 0 0 * * *`: Every day at midnight
- `0 0 0 * * 1-5`: Every weekday at midnight
- `0 30 9 * * *`: Every day at 9:30 AM

## Run Locally
- `func start` will trigger the function based on the schedule.
- For immediate testing without waiting for the schedule, use the admin endpoint:
  `POST http://localhost:7071/admin/functions/<function_name>` 
  with body `{"input": "test"}` and header `Content-Type: application/json`.

## Production Considerations
- CRON expressions: use Azure Functions NCRONTAB format (6 fields including seconds).
- Timezone: configure WEBSITE_TIME_ZONE app setting for non-UTC schedules. UTC is the default.
- Execution guarantees: timer triggers are at-least-once; design for idempotency.
- Timeout: default 5 minutes on consumption plan; configure functionTimeout in host.json.
- Singleton lock: timer functions use a blob lease to prevent concurrent execution across instances.
- Missed schedules: set runOnStartup cautiously (can cause unexpected executions on deployment).
- Monitoring: track execution duration and failures in Application Insights.
- Long-running tasks: if task exceeds timeout, consider offloading to a Durable Function orchestrator.
- Scale out: timer functions run as a single instance (singleton) across all scaled-out instances.
- Dependencies: ensure any external systems polled by the timer can handle the periodic load.
- Logging: use informative logs to track the start and end of long-running scheduled tasks.

## Scaffold Starter
```bash
azure-functions-scaffold new my-timer --template timer-job
```

## Testing
Test the logic of your timer function independently of the trigger.

```python
import unittest
from unittest.mock import MagicMock
import azure.functions as func
from function_app import timer_trigger_function

class TestTimerJob(unittest.TestCase):
    def test_timer_logic_execution(self):
        # Arrange
        mock_timer = MagicMock(spec=func.TimerRequest)
        mock_timer.past_due = False
        
        # Act
        timer_trigger_function(mock_timer)
        
        # Assert
        # Verify your maintenance logic was triggered
        pass
```

## Advanced Configuration
- Use `use_monitor=True` to persist the timer's schedule across restarts.
- Set `run_on_startup=True` if the task must run immediately when the app starts.
- Configure `WEBSITE_TIME_ZONE` in Azure App Service settings for local time scheduling.
- Use `Application Insights` to set up alerts for functions that fail to complete.
- Adjust `functionTimeout` in host.json if your tasks consistently take longer than 5 minutes.
- For very high frequency tasks (every few seconds), consider a queue worker with a delay instead.
- Monitor the storage account used for the timer lease to avoid performance issues.
- Ensure that the connection string `AzureWebJobsStorage` is correctly configured.
- Avoid using timer triggers for tasks that could be event-driven (like file processing).
- Review logs periodically to ensure the CRON expression is behaving as expected.
- Implement error handling to prevent a single failure from blocking future executions.
- Use environment variables for sensitive configuration used within the task.
- Document the purpose and frequency of each timer job for maintenance.
- Coordinate schedules to avoid overwhelming shared resources at the same time.
- Consider using a retry policy for transient errors within the task logic.
- Validate that the function name in the admin endpoint matches the function's name.
- Be aware of cold start impacts if the schedule is very infrequent.
- Use Managed Identities to access Azure resources from your timer function.
- Test your CRON expressions using online tools that support the 6-field format.
- Ensure the function app has sufficient permissions to write to its storage account.
