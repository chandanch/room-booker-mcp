from enum import StrEnum


class Permission(StrEnum):
    ROOM_READ = "Room.Read"

    BOOKING_CREATE = "Booking.Create"
    BOOKING_READ_SELF = "Booking.ReadSelf"
    BOOKING_UPDATE_SELF = "Booking.UpdateSelf"
    BOOKING_CANCEL_SELF = "Booking.CancelSelf"

    BOOKING_ADMIN = "Booking.Admin"


class EntraRole(StrEnum):
    READ_ONLY = "RoomBooking.ReadOnly"
    USER = "RoomBooking.User"
    ADMIN = "RoomBooking.Admin"


ROLE_PERMISSIONS: dict[EntraRole, set[Permission]] = {
    EntraRole.READ_ONLY: {
        Permission.ROOM_READ,
    },
    EntraRole.USER: {
        Permission.ROOM_READ,
        Permission.BOOKING_CREATE,
        Permission.BOOKING_READ_SELF,
        Permission.BOOKING_UPDATE_SELF,
        Permission.BOOKING_CANCEL_SELF,
    },
    EntraRole.ADMIN: {
        Permission.ROOM_READ,
        Permission.BOOKING_CREATE,
        Permission.BOOKING_READ_SELF,
        Permission.BOOKING_UPDATE_SELF,
        Permission.BOOKING_CANCEL_SELF,
        Permission.BOOKING_ADMIN,
    },
}


def resolve_permissions(
    role_values: set[str],
) -> set[str]:
    permissions: set[Permission] = set()

    for role in EntraRole:
        if role.value in role_values:
            permissions.update(ROLE_PERMISSIONS[role])

    return {permission.value for permission in permissions}
