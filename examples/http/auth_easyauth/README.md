# auth_easyauth

EasyAuth principal extraction with role-based access control for Azure Functions.

## Prerequisites

- Python 3.10+
- [Azure Functions Core Tools v4](https://learn.microsoft.com/azure/azure-functions/functions-run-local)
- [Azurite](https://learn.microsoft.com/azure/storage/common/storage-use-azurite) (local Storage emulator)
- App Service Authentication (EasyAuth) enabled on the Function App

## What It Demonstrates

- Decoding the `X-MS-CLIENT-PRINCIPAL` header (base64-encoded JSON)
- Extracting user claims, identity provider, and user ID
- Role-based access control using the `roles` claim
- Returning 401 for unauthenticated requests and 403 for unauthorized requests

## Run Locally

```bash
cd examples/http/auth_easyauth
python -m venv .venv
source .venv/bin/activate
pip install -e .
cp local.settings.json.example local.settings.json
func start
```

> **Note:** Locally, the `X-MS-CLIENT-PRINCIPAL` header is not injected by
> App Service. You can test by manually passing a base64-encoded principal
> in the header (see Expected Output below).

## Expected Output Example

```bash
# Encode a test principal
PRINCIPAL=$(echo -n '{"identityProvider":"aad","userId":"user-1","claims":[{"typ":"name","val":"Alice"},{"typ":"roles","val":"admin"}]}' | base64)

# Get user claims
curl -s "http://localhost:7071/api/auth/me" \
  -H "X-MS-CLIENT-PRINCIPAL: $PRINCIPAL" | python -m json.tool
```

```json
{
    "identity_provider": "aad",
    "user_id": "user-1",
    "claims": {
        "name": "Alice",
        "roles": "admin"
    },
    "roles": ["admin"]
}
```

```bash
# Access admin endpoint
curl -s "http://localhost:7071/api/auth/admin" \
  -H "X-MS-CLIENT-PRINCIPAL: $PRINCIPAL" | python -m json.tool
```

```json
{
    "message": "Welcome, admin!",
    "user_id": "user-1"
}
```
