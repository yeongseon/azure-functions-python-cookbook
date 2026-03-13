# GitHub Webhook Receiver Example

Secure webhook endpoint that validates HMAC-SHA256 signatures and routes
GitHub events to handler functions.

This example demonstrates:
- HMAC-SHA256 signature validation using `X-Hub-Signature-256`
- Event routing based on `X-GitHub-Event` header
- Handlers for push, pull_request, and issues events
- Delivery tracking via `X-GitHub-Delivery` header

Set the `GITHUB_WEBHOOK_SECRET` environment variable (or add it to
`local.settings.json`) before running.

This project corresponds to the `recipes/github-webhook.md` recipe.

## Run Locally

```bash
pip install -r requirements.txt
func start
```
