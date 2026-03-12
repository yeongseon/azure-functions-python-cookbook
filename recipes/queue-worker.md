# Queue Worker

## Overview
A background processing function triggered by Azure Storage Queue messages. This recipe demonstrates how to build reliable, asynchronous job processing using queue bindings. Messages placed on a queue are automatically picked up and processed by the function, enabling decoupled architectures where HTTP endpoints can return immediately while heavy work happens in the background.

## When to Use
- Offloading long-running tasks from HTTP handlers
- Processing events asynchronously (order processing, email sending, image resizing)
- Building producer-consumer patterns
- Handling bursty workloads with automatic scaling

## Architecture
- Producer (HTTP function or external system) enqueues a message
- Azure Storage Queue holds messages until a worker picks them up
- Queue-triggered function processes each message
- Failed messages are retried automatically and eventually moved to a poison queue

ASCII diagram:
```text
Producer -> Azure Storage Queue -> Queue Worker Function -> Output
                                       |
                                  Poison Queue (on failure)
```

## Project Structure
```text
queue-worker/
  function_app.py       # Queue-triggered function
  host.json
  local.settings.json   # Queue connection string
  requirements.txt
  tests/
    test_worker.py
```

## Implementation

### Python Code Example
The following code demonstrates a Python v2 model function that triggers on a queue named "work-items".

```python
import azure.functions as func
import logging
import json

app = func.FunctionApp()

@app.queue_trigger(arg_name="msg", 
                  queue_name="work-items", 
                  connection="AzureWebJobsStorage")
def process_queue_message(msg: func.QueueMessage) -> None:
    logging.info('Python Queue trigger function processed a message.')
    
    try:
        # Get the message body
        message_body = msg.get_body().decode('utf-8')
        logging.info(f"Message content: {message_body}")
        
        # Parse JSON payload if applicable
        data = json.loads(message_body)
        
        # Perform background processing logic here
        # Example: update database, send email, process image
        process_task(data)
        
    except json.JSONDecodeError:
        logging.error("Failed to decode JSON from queue message.")
    except Exception as e:
        logging.error(f"Error processing message: {str(e)}")
        # Raising an exception will trigger the built-in retry mechanism
        raise

def process_task(data):
    # Business logic implementation
    pass
```

### Configuration (host.json)
Configure queue behavior in your host.json file to optimize performance.

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

## Run Locally
- Requires Azurite (Azure Storage emulator) for local queue
- Configure "AzureWebJobsStorage": "UseDevelopmentStorage=true" in local.settings.json
- Start Azurite in a separate terminal: azurite --queue-port 10001
- Run the function app: func start
- Add a message to the "work-items" queue using Azure Storage Explorer or Azure CLI

## Production Considerations
- Message visibility timeout: configure based on expected processing time. If the function takes longer than this timeout, another instance might pick up the same message.
- Poison queue handling: monitor and alert on poison queue depth. A "work-items-poison" queue is created automatically after a message fails maxDequeueCount times.
- Idempotency: design handlers to be safe for duplicate processing. Network issues or timeouts can lead to a message being processed more than once.
- Scaling: the consumption plan scales based on queue depth. Large backlogs trigger the scale controller to add more instances.
- Message size: max 64 KB per message. For larger payloads, store the data in Azure Blob Storage and pass a reference (URI) in the queue message.
- Batch processing: configure maxBatchSize in host.json for throughput. Higher numbers increase throughput but might increase memory usage.
- Dead letter handling: implement monitoring for failed messages in the poison queue. Use a separate process or manual intervention to resolve issues.
- Ordering: Azure Storage Queues do not guarantee strict first-in-first-out (FIFO) ordering. If order is critical, consider Azure Service Bus sessions.
- Storage account limits: be aware of storage account IOPS limits when running high-volume queue workloads.

## Scaffold Starter
```bash
azure-functions-scaffold new my-worker --template queue-worker
```

## Testing
Use the following test pattern for your queue worker.

```python
import unittest
from unittest.mock import MagicMock
import azure.functions as func
from function_app import process_queue_message

class TestQueueWorker(unittest.TestCase):
    def test_process_message_success(self):
        # Arrange
        mock_msg = MagicMock(spec=func.QueueMessage)
        mock_msg.get_body.return_value = b'{"id": "123", "action": "test"}'
        
        # Act
        process_queue_message(mock_msg)
        
        # Assert
        # Verify that your processing logic was called correctly
        pass
```

## Monitoring and Logging
- Use Application Insights to track execution success rates and latency.
- Log the Message ID and Pop Receipt for traceability across different systems.
- Monitor the 'QueueLength' metric in the storage account to identify scaling bottlenecks.
- Check the 'DequeueCount' in the message to detect retries.
- Implement custom metrics for business-specific tracking (e.g., jobs completed).
- Use structured logging to simplify log analysis in Azure Log Analytics.
- Set appropriate log levels in host.json to avoid excessive costs while maintaining visibility.
- Monitor storage account transaction costs, especially with short polling intervals.
- Establish alerts for high failure rates or excessive processing times.
- Document the schema of your queue messages to maintain contract consistency.
- Implement versioning for message schemas if you anticipate breaking changes.
- Consider message encryption for sensitive data stored in queues.
- Use Azure Managed Identities for secure access to the storage account.
- Periodically review and purge old poison queue messages if they are not actionable.
- Ensure your worker function is deployed in the same region as your storage account.
