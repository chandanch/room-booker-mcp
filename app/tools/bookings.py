from datetime import datetime

from app.auth.context import get_current_user
from app.auth.exceptions import AuthorizationError
from app.auth.permissions import Permission
from app.models import Booking
from app.policies.tool_policy import require_permission
from app.services.booking_store import (
    create_booking,
    delete_booking,
    get_booking,
    list_bookings_for_user,
    update_booking,
)


def register_booking_tools(mcp):
    @mcp.tool
    def book_room(
        room_id: str,
        title: str,
        start_time: datetime,
        end_time: datetime,
        attendees_count: int,
    ):
        """
        Book a room for the authenticated user.
        """
        user = get_current_user()
        require_permission(user, Permission.BOOKING_CREATE)

        booking = Booking(
            booking_id="",
            room_id=room_id,
            user_id=user.user_id,
            title=title,
            start_time=start_time,
            end_time=end_time,
            attendees_count=attendees_count,
        )

        return create_booking(booking)

    @mcp.tool
    def get_my_bookings():
        """
        Return bookings owned by the authenticated user.
        """
        user = get_current_user()
        require_permission(user, Permission.BOOKING_READ_SELF)

        return list_bookings_for_user(user.user_id)

    @mcp.tool
    def update_my_booking(
        booking_id: str,
        title: str,
        start_time: datetime,
        end_time: datetime,
        attendees_count: int,
    ):
        """
        Update a booking owned by the authenticated user.
        """
        user = get_current_user()
        require_permission(
            user,
            Permission.BOOKING_UPDATE_SELF,
        )

        existing_booking = get_booking(booking_id)

        if existing_booking is None:
            raise ValueError("Booking not found")

        if existing_booking.user_id != user.user_id:
            raise AuthorizationError("You cannot update another user's booking")

        updated_booking = existing_booking.model_copy(
            update={
                "title": title,
                "start_time": start_time,
                "end_time": end_time,
                "attendees_count": attendees_count,
            }
        )

        return update_booking(updated_booking)

    @mcp.tool
    def cancel_my_booking(booking_id: str):
        """
        Cancel a booking owned by the authenticated user.
        """
        user = get_current_user()
        require_permission(
            user,
            Permission.BOOKING_CANCEL_SELF,
        )

        booking = get_booking(booking_id)

        if booking is None:
            raise ValueError("Booking not found")

        if booking.user_id != user.user_id:
            raise AuthorizationError("You cannot cancel another user's booking")

        return {
            "booking_id": booking_id,
            "cancelled": delete_booking(booking_id),
        }

    @mcp.tool
    def admin_cancel_booking(
        booking_id: str,
        reason: str,
    ):
        """
        Administratively cancel any booking.
        """
        user = get_current_user()
        require_permission(user, Permission.BOOKING_ADMIN)

        booking = get_booking(booking_id)

        if booking is None:
            raise ValueError("Booking not found")

        cancelled = delete_booking(booking_id)

        return {
            "booking_id": booking_id,
            "cancelled": cancelled,
            "cancelled_by": user.user_id,
            "reason": reason,
        }
