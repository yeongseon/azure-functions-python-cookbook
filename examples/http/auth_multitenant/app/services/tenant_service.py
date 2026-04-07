from __future__ import annotations

import base64
import json
from typing import Any

import azure.functions as func


def _json_response(body: object, status_code: int = 200) -> func.HttpResponse:
    return func.HttpResponse(
        body=json.dumps(body),
        status_code=status_code,
        mimetype="application/json",
    )


def decode_client_principal(header_value: str | None) -> dict[str, Any] | None:
    """Decode the X-MS-CLIENT-PRINCIPAL header from base64 JSON.

    Returns the parsed principal dict, or None if the header is missing or invalid.
    """
    if not header_value:
        return None
    try:
        decoded = base64.b64decode(header_value)
        return json.loads(decoded)
    except (ValueError, json.JSONDecodeError):
        return None


def extract_tenant_id(principal: dict[str, Any]) -> str | None:
    """Extract the tenant ID from the principal claims.

    Looks for a claim with typ ``tid`` or
    ``http://schemas.microsoft.com/identity/claims/tenantid``.
    """
    for claim in principal.get("claims", []):
        typ = claim.get("typ", "")
        if typ in ("tid", "http://schemas.microsoft.com/identity/claims/tenantid"):
            val = claim.get("val", "")
            if val:
                return val
    return None


def parse_allowed_tenants(raw: str) -> list[str]:
    """Parse a comma-separated list of allowed tenant IDs.

    Strips whitespace and ignores empty entries.
    """
    if not raw:
        return []
    return [t.strip() for t in raw.split(",") if t.strip()]


def is_tenant_allowed(tenant_id: str, allowed_tenants: list[str]) -> bool:
    """Check whether a tenant ID is in the allowlist.

    An empty allowlist means no tenants are allowed.
    """
    return tenant_id in allowed_tenants


def get_data_response(
    principal: dict[str, Any], tenant_id: str
) -> tuple[dict[str, Any], int]:
    """Build the response body for the /auth/data endpoint."""
    return {
        "message": "Access granted.",
        "tenant_id": tenant_id,
        "user_id": principal.get("userId", "unknown"),
        "identity_provider": principal.get("identityProvider", "unknown"),
    }, 200
