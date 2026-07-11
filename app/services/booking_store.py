from uuid import uuid4
from app.models import Room, Booking

ROOMS = [
    Room(room_id="blr-101", name="Bangalore Room 101", location="BLR", capacity=4),
    Room(room_id="blr-201", name="Bangalore Board Room", location="BLR", capacity=12),
    Room(room_id="mum-101", name="Mumbai Focus Room", location="MUM", capacity=3),
]

BOOKINGS: list[Booking] = []


def list_rooms() -> list[Room]:
    return ROOMS


def get_room(room_id: str) -> Room | None:
    return next((room for room in ROOMS if room.room_id == room_id), None)


def list_bookings_for_user(user_id: str) -> list[Booking]:
    return [booking for booking in BOOKINGS if booking.user_id == user_id]


def create_booking(booking: Booking) -> Booking:
    booking.booking_id = str(uuid4())
    BOOKINGS.append(booking)
    return booking


def cancel_booking(booking_id: str, user_id: str, is_admin: bool = False) -> bool:
    for booking in BOOKINGS:
        if booking.booking_id == booking_id:
            if booking.user_id != user_id and not is_admin:
                raise PermissionError("Cannot cancel another user's booking")
            BOOKINGS.remove(booking)
            return True
    return False
