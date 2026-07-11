from app.services.booking_store import list_rooms, get_room


def register_room_tools(mcp):
    @mcp.tool
    def search_rooms(location: str | None = None, min_capacity: int | None = None):
        rooms = list_rooms()

        if location:
            rooms = [
                room for room in rooms if room.location.lower() == location.lower()
            ]

        if min_capacity:
            rooms = [room for room in rooms if room.capacity >= min_capacity]

        return rooms

    @mcp.tool
    def get_room_details(room_id: str):
        room = get_room(room_id)
        if not room:
            raise ValueError("Room not found")
        return room
