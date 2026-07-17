from uuid import uuid4

from app.models import Booking, Room

ROOMS = [
    Room(
        room_id="blr-101",
        name="Bangalore Room 101",
        location="BLR",
        capacity=4,
    ),
    Room(
        room_id="blr-201",
        name="Bangalore Board Room",
        location="BLR",
        capacity=12,
    ),
    Room(
        room_id="mum-101",
        name="Mumbai Focus Room",
        location="MUM",
        capacity=3,
    ),
]


BOOKINGS: list[Booking] = []


def list_rooms() -> list[Room]:
    return ROOMS.copy()


def get_room(room_id: str) -> Room | None:
    return next(
        (room for room in ROOMS if room.room_id == room_id),
        None,
    )


def get_booking(booking_id: str) -> Booking | None:
    return next(
        (booking for booking in BOOKINGS if booking.booking_id == booking_id),
        None,
    )


def list_bookings_for_user(user_id: str) -> list[Booking]:
    return [booking for booking in BOOKINGS if booking.user_id == user_id]


def list_bookings_for_room(room_id: str) -> list[Booking]:
    return [booking for booking in BOOKINGS if booking.room_id == room_id]


def create_booking(booking: Booking) -> Booking:
    stored_booking = booking.model_copy(update={"booking_id": str(uuid4())})

    BOOKINGS.append(stored_booking)
    return stored_booking


def update_booking(updated_booking: Booking) -> Booking:
    for index, existing_booking in enumerate(BOOKINGS):
        if existing_booking.booking_id == updated_booking.booking_id:
            BOOKINGS[index] = updated_booking
            return updated_booking

    raise ValueError("Booking not found")


def delete_booking(booking_id: str) -> bool:
    booking = get_booking(booking_id)

    if booking is None:
        return False

    BOOKINGS.remove(booking)
    return True


def clear_bookings() -> None:
    """
    Intended for tests only.
    """
    BOOKINGS.clear()
