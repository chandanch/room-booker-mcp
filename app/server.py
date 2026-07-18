from dotenv import load_dotenv
from fastmcp import FastMCP

from app.tools.bookings import register_booking_tools
from app.tools.rooms import register_room_tools

load_dotenv()

mcp = FastMCP("room-booking-mcp")

register_room_tools(mcp)
register_booking_tools(mcp)


if __name__ == "__main__":
    mcp.run()
