import pytest

from app.auth.exceptions import AuthorizationError
from app.auth.permissions import Permission
from app.models import UserContext
from app.policies.tool_policy import (
    require_any_permission,
    require_permission,
)


def test_user_with_permission_is_allowed():
    user = UserContext(
        user_id="user-001",
        scopes={"Booking.Create"},
    )

    require_permission(
        user,
        Permission.BOOKING_CREATE,
    )


def test_user_without_permission_is_denied():
    user = UserContext(
        user_id="user-001",
        scopes={"Room.Read"},
    )

    with pytest.raises(
        AuthorizationError,
        match="Booking.Create",
    ):
        require_permission(
            user,
            Permission.BOOKING_CREATE,
        )


def test_application_role_is_accepted():
    service_principal = UserContext(
        user_id="service-principal-001",
        roles={"Booking.Admin"},
    )

    require_permission(
        service_principal,
        Permission.BOOKING_ADMIN,
    )


def test_require_any_permission():
    user = UserContext(
        user_id="user-001",
        scopes={"Booking.ReadSelf"},
    )

    require_any_permission(
        user,
        Permission.BOOKING_READ_SELF,
        Permission.BOOKING_ADMIN,
    )


def test_require_any_permission_rejects_user():
    user = UserContext(
        user_id="user-001",
        scopes={"Room.Read"},
    )

    with pytest.raises(AuthorizationError):
        require_any_permission(
            user,
            Permission.BOOKING_READ_SELF,
            Permission.BOOKING_ADMIN,
        )
