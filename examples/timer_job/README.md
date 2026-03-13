# Timer Scheduled Job Example

Time-triggered function that runs on a configurable CRON schedule.

This example demonstrates:
- Timer trigger with NCRONTAB expression (`0 */5 * * * *` = every 5 minutes)
- Past-due detection for missed executions
- Schedule monitoring via `use_monitor=True`
- Periodic maintenance task pattern

This project corresponds to the `recipes/timer-job.md` recipe.

## Run Locally

```bash
pip install -r requirements.txt
func start
# Or trigger manually:
# curl -X POST http://localhost:7071/admin/functions/scheduled_job \
#   -H "Content-Type: application/json" -d '{"input": "test"}'
```
