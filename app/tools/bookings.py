from datetime import datetime
from app.models import Booking
from app.services.booking_store import (
    create_booking,
    list_bookings_for_user,
    cancel_booking,
)


def register_booking_tools(mcp):
    @mcp.tool
    def book_room(
        room_id: str,
        user_id: str,
        title: str,
        start_time: datetime,
        end_time: datetime,
        attendees_count: int,
    ):
        booking = Booking(
            booking_id="",
            room_id=room_id,
            user_id=user_id,
            title=title,
            start_time=start_time,
            end_time=end_time,
            attendees_count=attendees_count,
        )
        return create_booking(booking)

    @mcp.tool
    def get_my_bookings(user_id: str):
        return list_bookings_for_user(user_id)

    @mcp.tool
    def cancel_my_booking(booking_id: str, user_id: str):
        return {"cancelled": cancel_booking(booking_id, user_id)}
