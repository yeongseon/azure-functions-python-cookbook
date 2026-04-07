from __future__ import annotations

import logging
from collections.abc import Mapping
from typing import cast

import azure.functions as func

from app.services.auth_service import (
    decode_client_principal,
    get_admin_response,
    get_user_claims_response,
    json_response,
)

auth_blueprint = func.Blueprint()

def auth_me(req: func.HttpRequest) -> func.HttpResponse:
    """Return the decoded EasyAuth principal claims."""
    headers = cast(Mapping[str, str], req.headers)
    header = headers.get("X-MS-CLIENT-PRINCIPAL")
    principal = decode_client_principal(header)
    if principal is None:
        logging.warning("No X-MS-CLIENT-PRINCIPAL header found.")
        return json_response(
            {"error": "Not authenticated. Missing X-MS-CLIENT-PRINCIPAL header."},
            status_code=401,
        )

    body, status_code = get_user_claims_response(principal)
    return json_response(body, status_code=status_code)

def auth_admin(req: func.HttpRequest) -> func.HttpResponse:
    """Return admin-only content after role check."""
    headers = cast(Mapping[str, str], req.headers)
    header = headers.get("X-MS-CLIENT-PRINCIPAL")
    principal = decode_client_principal(header)
    if principal is None:
        logging.warning("No X-MS-CLIENT-PRINCIPAL header found.")
        return json_response(
            {"error": "Not authenticated. Missing X-MS-CLIENT-PRINCIPAL header."},
            status_code=401,
        )

    body, status_code = get_admin_response(principal)
    return json_response(body, status_code=status_code)


auth_blueprint.route(route="auth/me", methods=["GET"], auth_level=func.AuthLevel.ANONYMOUS)(auth_me)
auth_blueprint.route(
    route="auth/admin", methods=["GET"], auth_level=func.AuthLevel.ANONYMOUS
)(auth_admin)
