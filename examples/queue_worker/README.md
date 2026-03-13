# Queue Worker Example

Background processing function triggered by Azure Storage Queue messages.

This example demonstrates:
- Queue trigger binding with `@app.queue_trigger`
- JSON message parsing and error handling
- Dequeue count tracking for retry awareness
- Configurable queue polling and visibility timeout in `host.json`

Configure `AzureWebJobsStorage` in `local.settings.json` or use Azurite
for local development.

This project corresponds to the `recipes/queue-worker.md` recipe.

## Run Locally

```bash
pip install -r requirements.txt
# Start Azurite for local queue emulation:
# azurite --queuePort 10001
func start
```
