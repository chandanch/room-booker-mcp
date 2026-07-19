from typing import Any

from fastmcp.server.dependencies import get_access_token

from app.auth.exceptions import AuthenticationError
from app.auth.permissions import resolve_permissions
from app.models import UserContext


def _as_string_set(value: Any) -> set[str]:
    if value is None:
        return set()

    if isinstance(value, str):
        return {item for item in value.split() if item}

    if isinstance(value, list):
        return {str(item) for item in value if item}

    raise AuthenticationError("Unexpected claim format in access token")


def get_current_user() -> UserContext:
    access_token = get_access_token()

    if access_token is None:
        raise AuthenticationError("No authenticated access token is available")

    claims = access_token.claims or {}

    tenant_id = claims.get("tid")
    object_id = claims.get("oid")
    subject = claims.get("sub")

    # For Entra workforce users, oid + tid is the preferred stable identity.
    principal_id = object_id or subject

    if not tenant_id:
        raise AuthenticationError("Access token does not contain a tenant ID")

    if not principal_id:
        raise AuthenticationError(
            "Access token does not contain a stable subject identifier"
        )

    token_scopes = _as_string_set(claims.get("scp"))
    entra_roles = _as_string_set(claims.get("roles"))
    permissions = resolve_permissions(entra_roles)

    return UserContext(
        user_id=f"{tenant_id}:{principal_id}",
        tenant_id=tenant_id,
        email=(claims.get("preferred_username") or claims.get("email")),
        name=claims.get("name"),
        scopes=permissions,
        roles=entra_roles,
    )
