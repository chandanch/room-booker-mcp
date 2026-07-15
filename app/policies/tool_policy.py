from app.auth.exceptions import AuthorizationError
from app.auth.permissions import Permission
from app.models import UserContext


def require_permission(
    user: UserContext,
    permission: Permission,
) -> None:
    """
    Verify that the current authenticated principal has the required
    delegated scope or application role.
    """

    if permission.value not in user.permissions:
        raise AuthorizationError(
            f"Permission denied. Required permission: {permission.value}"
        )


def require_any_permission(
    user: UserContext,
    *permissions: Permission,
) -> None:
    required = {permission.value for permission in permissions}

    if user.permissions.isdisjoint(required):
        raise AuthorizationError(
            "Permission denied. At least one of these permissions "
            f"is required: {sorted(required)}"
        )


def require_admin(user: UserContext) -> None:
    require_permission(user, Permission.BOOKING_ADMIN)
