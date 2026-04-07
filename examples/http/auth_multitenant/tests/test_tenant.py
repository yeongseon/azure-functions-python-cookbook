import base64
import json

from app.services.tenant_service import (
    decode_client_principal,
    extract_tenant_id,
    get_data_response,
    is_tenant_allowed,
    parse_allowed_tenants,
)


def _make_principal(
    claims: list[dict[str, str]] | None = None,
    user_id: str = "user-1",
    identity_provider: str = "aad",
) -> dict[str, object]:
    return {
        "identityProvider": identity_provider,
        "userId": user_id,
        "claims": claims or [],
    }


def _encode_principal(principal: dict[str, object]) -> str:
    return base64.b64encode(json.dumps(principal).encode()).decode()


def test_decode_client_principal_valid() -> None:
    principal = _make_principal()
    encoded = _encode_principal(principal)
    result = decode_client_principal(encoded)
    assert result is not None
    assert result["userId"] == "user-1"


def test_decode_client_principal_none() -> None:
    assert decode_client_principal(None) is None


def test_decode_client_principal_invalid() -> None:
    assert decode_client_principal("not-valid!!!") is None


def test_extract_tenant_id_with_tid() -> None:
    principal = _make_principal(claims=[{"typ": "tid", "val": "tenant-abc"}])
    assert extract_tenant_id(principal) == "tenant-abc"


def test_extract_tenant_id_with_long_form() -> None:
    principal = _make_principal(claims=[
        {"typ": "http://schemas.microsoft.com/identity/claims/tenantid", "val": "tenant-xyz"},
    ])
    assert extract_tenant_id(principal) == "tenant-xyz"


def test_extract_tenant_id_missing() -> None:
    principal = _make_principal(claims=[{"typ": "name", "val": "Alice"}])
    assert extract_tenant_id(principal) is None


def test_parse_allowed_tenants() -> None:
    result = parse_allowed_tenants("tenant-a, tenant-b, tenant-c")
    assert result == ["tenant-a", "tenant-b", "tenant-c"]


def test_parse_allowed_tenants_empty() -> None:
    assert parse_allowed_tenants("") == []


def test_parse_allowed_tenants_with_blanks() -> None:
    result = parse_allowed_tenants("tenant-a,,, tenant-b,")
    assert result == ["tenant-a", "tenant-b"]


def test_is_tenant_allowed_true() -> None:
    assert is_tenant_allowed("tenant-a", ["tenant-a", "tenant-b"]) is True


def test_is_tenant_allowed_false() -> None:
    assert is_tenant_allowed("tenant-c", ["tenant-a", "tenant-b"]) is False


def test_is_tenant_allowed_empty_list() -> None:
    assert is_tenant_allowed("tenant-a", []) is False


def test_get_data_response() -> None:
    principal = _make_principal()
    body, status = get_data_response(principal, "tenant-abc")
    assert status == 200
    assert body["tenant_id"] == "tenant-abc"
    assert body["user_id"] == "user-1"
    assert body["message"] == "Access granted."
