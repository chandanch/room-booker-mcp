from datetime import datetime

from app.auth.context import get_current_user
from app.auth.permissions import Permission
from app.policies.tool_policy import require_permission
from app.services.booking_store import (
    get_room,
    list_bookings_for_room,
    list_rooms,
)


def register_room_tools(mcp):
    @mcp.tool
    def search_rooms(
        location: str | None = None,
        min_capacity: int | None = None,
    ):
        """
        Search meeting rooms by location and minimum capacity.
        """
        user = get_current_user()
        require_permission(user, Permission.ROOM_READ)

        rooms = list_rooms()

        if location:
            rooms = [
                room
                for room in rooms
                if room.location.casefold() == location.casefold()
            ]

        if min_capacity is not None:
            rooms = [room for room in rooms if room.capacity >= min_capacity]

        return rooms

    @mcp.tool
    def get_room_details(room_id: str):
        """
        Retrieve details for a single meeting room.
        """
        user = get_current_user()
        require_permission(user, Permission.ROOM_READ)

        room = get_room(room_id)

        if room is None:
            raise ValueError(f"Room not found: {room_id}")

        return room

    @mcp.tool
    def get_room_availability(
        room_id: str,
        start_time: datetime,
        end_time: datetime,
    ):
        """
        Check whether a room has overlapping bookings.
        """
        user = get_current_user()
        require_permission(user, Permission.ROOM_READ)

        room = get_room(room_id)

        if room is None:
            raise ValueError(f"Room not found: {room_id}")

        overlapping_bookings = [
            booking
            for booking in list_bookings_for_room(room_id)
            if (booking.start_time < end_time and booking.end_time > start_time)
        ]

        return {
            "room_id": room_id,
            "available": len(overlapping_bookings) == 0,
            "conflicting_booking_count": len(overlapping_bookings),
        }
