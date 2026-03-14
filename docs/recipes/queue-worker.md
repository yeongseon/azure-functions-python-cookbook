# Queue Worker

## Overview

This recipe demonstrates asynchronous background processing with an Azure
Storage Queue trigger. A producer writes messages to a queue, and the worker
function processes each message independently.

The paired runnable project is `examples/queue_worker`.

## Primary use case

Use this pattern when you need:

- long-running operations moved out of HTTP request path
- burst handling through queued backlog
- retry-aware processing with dequeue counts
- producer/consumer separation between services

## Architecture diagram (text)

```text
Producer (HTTP app / external system)
  |
  | enqueue JSON message
  v
Azure Storage Queue (work-items)
  |
  | trigger
  v
process_queue_message(msg)
  |- decode bytes to text
  |- parse JSON payload
  |- process task data
  '- log result and dequeue metadata

Failure path:
  processing error -> runtime retry -> poison queue after max dequeue
```

## Prerequisites

- Python 3.10+
- Azure Functions Core Tools v4
- Azurite for local queue emulation (recommended)
- `AzureWebJobsStorage` configured for local environment

Install and run:

```bash
cd examples/queue_worker
pip install -r requirements.txt
func start
```

Start Azurite in another terminal:

```bash
azurite --queuePort 10001
```

## Step-by-step implementation guide

Implementation flow in `examples/queue_worker/function_app.py`:

1. Define `app = func.FunctionApp()` and logger.
2. Implement `_process_task(data)` for business logic.
3. Register queue trigger for queue `work-items`.
4. Read message id, dequeue count, and body bytes.
5. Decode bytes to UTF-8 text.
6. Parse JSON payload with error handling.
7. Execute processing function and write completion logs.

## Complete code walkthrough

### Worker setup and task processor

```python
import azure.functions as func
import json
import logging

app = func.FunctionApp()
logger = logging.getLogger(__name__)

def _process_task(data: dict) -> str:
    task_id = data.get("id", "unknown")
    action = data.get("action", "unknown")
    logger.info("Processing task %s: %s", task_id, action)
    return f"Completed task {task_id}"
```

`_process_task` is where real domain work would be performed.

### Queue trigger handler

```python
@app.queue_trigger(
    arg_name="msg",
    queue_name="work-items",
    connection="AzureWebJobsStorage",
)
def process_queue_message(msg: func.QueueMessage) -> None:
    message_id = msg.id
    body_bytes = msg.get_body()
    body_text = body_bytes.decode("utf-8")
    dequeue_count = msg.dequeue_count

    logger.info(
        "Received message %s (dequeue_count=%d): %s",
        message_id,
        dequeue_count,
        body_text,
    )

    try:
        data = json.loads(body_text)
    except (ValueError, json.JSONDecodeError):
        logger.error("Invalid JSON in message %s — skipping", message_id)
        return

    result = _process_task(data)
    logger.info("Message %s result: %s", message_id, result)
```

This is a practical baseline for safe queue payload handling.

## Running locally

### 1) Configure storage connection

Set local connection string to development storage in local settings.

```text
AzureWebJobsStorage=UseDevelopmentStorage=true
```

### 2) Start Azurite

```bash
azurite --queuePort 10001
```

### 3) Start worker

```bash
cd examples/queue_worker
pip install -r requirements.txt
func start
```

### 4) Enqueue a test message

Use any queue client/tool to push JSON text into `work-items`:

```json
{"id": "job-001", "action": "thumbnail"}
```

## Expected output

Typical logs after message arrival:

```text
Received message <id> (dequeue_count=1): {"id":"job-001","action":"thumbnail"}
Processing task job-001: thumbnail
Message <id> result: Completed task job-001
```

Invalid payload log path:

```text
Invalid JSON in message <id> — skipping
```

## Production considerations

- Keep handlers idempotent because retries can reprocess messages.
- Track dequeue count and alert on repeated failures.
- Route permanent failures to poison-queue remediation flow.
- Keep message schema compact and versioned.
- Put large payloads in blob storage and queue references only.
- Tune queue extension settings for throughput and latency.
- Add structured logging with message id and correlation id.
- Protect storage access with managed identity where possible.

!!! warning
    Do not assume strict FIFO ordering with Azure Storage Queues.

## Suggested host settings (from source recipe)

```json
{
  "version": "2.0",
  "extensions": {
    "queues": {
      "maxPollingInterval": "00:00:02",
      "visibilityTimeout": "00:00:30",
      "batchSize": 16,
      "maxDequeueCount": 5,
      "newBatchThreshold": 8
    }
  }
}
```

## Related recipes

- For request-facing APIs, see [HTTP API Basic](http-api-basic.md).
- For scheduled processing without producer messages, see [Timer Job](timer-job.md).

## Ecosystem links

- `azure-functions-logging` for traceable worker logs
- `azure-functions-validation` for payload schema checks
- `azure-functions-scaffold` for queue app bootstrapping
