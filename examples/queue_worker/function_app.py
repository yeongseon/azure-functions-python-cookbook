"""Queue worker that processes messages from Azure Storage Queue."""

from __future__ import annotations

import json
import logging

import azure.functions as func

app = func.FunctionApp()

logger = logging.getLogger(__name__)


def _process_task(data: dict) -> str:
    """Simulate processing a task from the queue message payload."""
    task_id = data.get("id", "unknown")
    action = data.get("action", "unknown")
    logger.info("Processing task %s: %s", task_id, action)
    return f"Completed task {task_id}"


@app.queue_trigger(
    arg_name="msg",
    queue_name="work-items",
    connection="AzureWebJobsStorage",
)
def process_queue_message(msg: func.QueueMessage) -> None:
    """Process a single message from the work-items queue."""
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
