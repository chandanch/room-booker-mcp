import os

from app.auth.exceptions import AuthenticationError
from app.models import UserContext

STANDARD_USER_PERMISSIONS = {
    "Room.Read",
    "Booking.Create",
    "Booking.ReadSelf",
    "Booking.UpdateSelf",
    "Booking.CancelSelf",
}


ADMIN_PERMISSIONS = {
    *STANDARD_USER_PERMISSIONS,
    "Booking.Admin",
}


def get_current_user() -> UserContext:
    """
    Temporary local identity provider.

    This function will be replaced in the Entra ID milestone.
    Tools and policies should not know whether the identity came from:
    - local development configuration,
    - an Entra ID token,
    - an API gateway,
    - or another identity provider.
    """

    mock_user = os.getenv("MOCK_USER", "employee").strip().lower()

    if mock_user == "anonymous":
        raise AuthenticationError("No authenticated user is available")

    if mock_user == "admin":
        return UserContext(
            user_id="entra-object-id-admin-001",
            email="room.admin@example.com",
            name="Room Administrator",
            tenant_id="mock-tenant-id",
            scopes=ADMIN_PERMISSIONS,
        )

    if mock_user == "employee":
        return UserContext(
            user_id="entra-object-id-user-001",
            email="chandan@example.com",
            name="Chandan",
            tenant_id="mock-tenant-id",
            scopes=STANDARD_USER_PERMISSIONS,
        )

    if mock_user == "readonly":
        return UserContext(
            user_id="entra-object-id-readonly-001",
            email="readonly@example.com",
            name="Read Only User",
            tenant_id="mock-tenant-id",
            scopes={"Room.Read"},
        )

    raise AuthenticationError(f"Unknown MOCK_USER value: {mock_user}")
