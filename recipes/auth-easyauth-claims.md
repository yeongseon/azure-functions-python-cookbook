# EasyAuth Claims Extraction

## Overview

This recipe demonstrates how to extract and use Azure App Service Authentication
(EasyAuth) claims in an Azure Functions Python v2 application. When EasyAuth is
enabled, authenticated requests arrive with the `X-MS-CLIENT-PRINCIPAL` header
containing a base64-encoded JSON payload with user identity, claims, and roles.

The example decodes this header, extracts claims into a usable format, and
implements role-based access control using the `roles` claim.

## When to Use

- Your Function App runs behind App Service Authentication (EasyAuth).
- You need to extract user identity (name, email, roles) from incoming requests.
- You want role-based access control without managing JWT validation yourself.
- You need a lightweight auth layer that complements — not replaces — EasyAuth.

## Architecture

```text
+-----------+   X-MS-CLIENT-PRINCIPAL   +----------------------------+
|  Client   | ------------------------> | App Service (EasyAuth)     |
+-----------+                           +------------+---------------+
                                                     |
                                                     | base64-encoded principal
                                                     v
                                        +----------------------------+
                                        | auth_me / auth_admin       |
                                        | (Azure Function handlers)  |
                                        +------------+---------------+
                                                     |
                                                     v
                                        +----------------------------+
                                        | auth_service               |
                                        | decode_client_principal()  |
                                        | extract_claims()           |
                                        | get_roles() / has_role()   |
                                        +----------------------------+
```

EasyAuth handles the OAuth2/OIDC login flow and token validation. Your function
only needs to read the injected header — no JWKS fetching or token parsing required.

## Prerequisites

- Python 3.10+
- Azure Functions Core Tools v4
- `azure-functions` package
- App Service Authentication (EasyAuth) enabled on the Function App

## Project Structure

```text
examples/http/auth_easyauth/
├── function_app.py
├── app/
│   ├── core/
│   │   └── logging.py
│   ├── functions/
│   │   └── auth.py
│   └── services/
│       └── auth_service.py
├── tests/
│   └── test_auth.py
├── host.json
├── local.settings.json.example
├── pyproject.toml
├── Makefile
└── README.md
```

## Implementation

### Decoding the principal header

The `X-MS-CLIENT-PRINCIPAL` header contains a base64-encoded JSON object with
`identityProvider`, `userId`, and a `claims` array of `{"typ": ..., "val": ...}`
objects:

```python
def decode_client_principal(header_value: str | None) -> Principal | None:
    if not header_value:
        return None
    try:
        decoded = base64.b64decode(header_value)
        parsed = json.loads(decoded)
    except (ValueError, json.JSONDecodeError):
        return None
    # Validate structure and return typed Principal dict
    ...
```

### Extracting claims and roles

Claims are flattened from the array format into a dictionary. Role claims use
the `roles` or `http://schemas.microsoft.com/ws/2008/06/identity/claims/role`
type:

```python
def extract_claims(principal: Principal) -> dict[str, str]:
    return {c["typ"]: c["val"] for c in principal.get("claims", []) if c.get("typ")}

def get_roles(principal: Principal) -> list[str]:
    role_types = ("roles", "http://schemas.microsoft.com/ws/2008/06/identity/claims/role")
    return [c["val"] for c in principal.get("claims", []) if c.get("typ") in role_types and c.get("val")]
```

### Role-based access control decorator

The `require_role` decorator enforces role checks before the handler runs:

```python
@require_role("admin")
def get_admin_response(principal: Principal) -> ServiceResponse:
    return {"message": "Welcome, admin!", "user_id": principal.get("userId", "unknown")}, 200
```

### Route handlers

Two endpoints demonstrate the pattern:

- `GET /api/auth/me` — returns decoded claims for any authenticated user.
- `GET /api/auth/admin` — requires the `admin` role, returns 403 otherwise.

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
> App Service. Test by manually passing a base64-encoded principal in the header.

## Expected Output

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
    "claims": {"name": "Alice", "roles": "admin"},
    "roles": ["admin"]
}
```

```bash
# Access admin endpoint (requires admin role)
curl -s "http://localhost:7071/api/auth/admin" \
  -H "X-MS-CLIENT-PRINCIPAL: $PRINCIPAL" | python -m json.tool
```

```json
{
    "message": "Welcome, admin!",
    "user_id": "user-1"
}
```

## Production Considerations

- **Scaling**: EasyAuth header decoding is CPU-trivial; this pattern adds no scaling concerns.
- **Security**: Never trust `X-MS-CLIENT-PRINCIPAL` from external sources. The header is only trustworthy when injected by App Service itself. In production, ensure the Function App is not directly accessible (use App Service networking controls).
- **Claim types**: Microsoft may use full URI claim types (e.g. `http://schemas.microsoft.com/...`). Always check both short and long forms.
- **Identity providers**: EasyAuth supports AAD, GitHub, Google, Facebook, and custom OpenID Connect. The principal format is consistent across providers, but available claims vary.
- **Observability**: Log the `identityProvider` and `userId` for audit trails. Avoid logging full claim payloads in production.

## Related Recipes

- [HTTP Auth Levels](./http-auth-levels.md)
- [JWT Bearer Validation](./auth-jwt-validation.md)
- [Multi-Tenant Auth](./auth-multitenant.md)
