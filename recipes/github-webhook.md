# GitHub Webhook Receiver

## Overview
An event-driven function that receives and processes GitHub webhook payloads. This recipe demonstrates how to build a secure webhook endpoint that validates incoming requests, parses event payloads, and triggers appropriate actions based on the event type. Using Azure Functions for this purpose is ideal because it allows you to only pay for the execution time when a GitHub event actually occurs, making it a cost-effective solution for automating your development workflows.

## When to Use
- Automating CI/CD workflows based on GitHub events like pushes or pull request updates.
- Tracking repository activity such as issue creation, PR comments, and branch deletions.
- Building ChatOps or notification systems that send alerts to Slack or Microsoft Teams.
- Integrating GitHub events with internal business systems or tracking tools.
- Managing repository configurations or permissions through automated scripts.
- Mirroring code or synchronizing data across different platforms in real-time.

## Architecture
- GitHub sends POST requests to the function endpoint on configured events.
- Function validates the webhook signature using the shared secret to ensure authenticity.
- Function parses the event type from the `X-GitHub-Event` header and the JSON body.
- Function dispatches to the appropriate handler logic based on the identified event type.

```text
+----------+       +-----------------------+       +-----------------------+
|  GitHub  | ----> |  Webhook POST Request | ----> | Azure Functions Host  |
+----------+       +-----------------------+       +-----------------------+
                                                              |
                                                              v
+----------+       +-----------------------+       +-----------------------+
|  Action  | <---- |    Event Router       | <---- |  function_app.py      |
+----------+       +-----------------------+       +-----------------------+
```

1. An event occurs in your GitHub repository (e.g., a pull request is opened).
2. GitHub sends a POST request with a JSON payload to your Function's URL.
3. Your function receives the request and immediately validates the signature.
4. The router identifies the event type and passes the payload to the correct handler.
5. The handler performs the necessary action, such as labeling a PR or triggering a build.

## Project Structure
```text
github-webhook/
  function_app.py       # Main entry point for the webhook function
  webhook_handler.py    # Logic for processing specific event types
  host.json             # Function host configuration settings
  local.settings.json   # Local secrets and shared webhook secret
  requirements.txt      # Dependencies including hmac and hashlib
  tests/                # Test suite for the webhook logic
    test_webhook.py     # Tests for signature validation and routing
```

## Implementation Detail

The most critical part of a webhook receiver is the signature validation. Below is an example of how to implement this securely in Python.

```python
import azure.functions as func
import hmac
import hashlib
import os

app = func.FunctionApp()

def validate_signature(payload, signature):
    secret = os.getenv("GITHUB_WEBHOOK_SECRET").encode()
    expected_signature = "sha256=" + hmac.new(
        secret, payload, hashlib.sha256
    ).hexdigest()
    return hmac.compare_digest(expected_signature, signature)

@app.route(route="github/webhook", methods=["POST"])
def github_webhook(req: func.HttpRequest) -> func.HttpResponse:
    signature = req.headers.get("X-Hub-Signature-256")
    event_type = req.headers.get("X-GitHub-Event")
    body = req.get_body()

    if not validate_signature(body, signature):
        return func.HttpResponse("Invalid signature", status_code=401)

    # Route the event
    if event_type == "pull_request":
        # Handle pull request event
        pass
    elif event_type == "push":
        # Handle push event
        pass

    return func.HttpResponse("Accepted", status_code=200)
```

## Run Locally
Running a webhook locally requires exposing your local development server to the internet so GitHub can reach it.

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Configure your local secret in `local.settings.json`:
   ```json
   {
     "Values": {
       "GITHUB_WEBHOOK_SECRET": "your-secret-here"
     }
   }
   ```

3. Start a tunnel (e.g., ngrok) to expose your local port (default 7071):
   ```bash
   ngrok http 7071
   ```

4. Start the function host:
   ```bash
   func start
   ```

5. Configure the webhook in GitHub using the ngrok URL.

## Production Considerations
- ALWAYS validate webhook signatures (HMAC-SHA256) to prevent spoofing from unknown sources.
- Use application settings for the webhook secret, never hardcode secrets in your repository.
- Handle duplicate deliveries idempotently; GitHub may retry a delivery if your function takes too long or fails.
- Log event types and delivery IDs for debugging and auditing purposes.
- Return a 200 OK response as quickly as possible. If your processing takes more than a few seconds, offload the heavy work to a storage queue or service bus.
- Rate limiting: GitHub may send bursts of events during high-activity periods. Ensure your function can scale appropriately.
- Check the `User-Agent` header to ensure it matches the expected GitHub format.
- Implement proper error handling to avoid revealing internal details in the response body.

## Scaffold Starter
You can quickly generate a project with GitHub webhook support using the following command:

```bash
azure-functions-scaffold new my-webhook --template github-webhook
```

## Security Best Practices
Security should be your top priority when dealing with webhooks. In addition to signature validation, you should regularly rotate your webhook secrets. You can also restrict the incoming traffic to GitHub's official IP ranges for an extra layer of protection. This can be done at the network level using Azure's networking features or directly within your function code.

## Idempotency
Because GitHub might retry a webhook delivery, your code should be able to handle the same event multiple times without side effects. For example, if you are posting a comment to a PR, you should first check if the comment already exists before posting it again. Using the delivery ID provided in the `X-GitHub-Delivery` header can help you track and ignore duplicate requests.
