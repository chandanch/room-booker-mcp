from enum import StrEnum


class Permission(StrEnum):
    ROOM_READ = "Room.Read"

    BOOKING_CREATE = "Booking.Create"
    BOOKING_READ_SELF = "Booking.ReadSelf"
    BOOKING_UPDATE_SELF = "Booking.UpdateSelf"
    BOOKING_CANCEL_SELF = "Booking.CancelSelf"

    BOOKING_ADMIN = "Booking.Admin"
