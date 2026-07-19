from fastmcp import FastMCP
from fastmcp.server.auth.providers.azure import AzureProvider

from app.config import get_settings
from app.tools.bookings import register_booking_tools
from app.tools.rooms import register_room_tools

settings = get_settings()

auth_provider = AzureProvider(
    client_id=settings.entra_client_id,
    client_secret=settings.entra_client_secret,
    tenant_id=settings.entra_tenant_id,
    base_url=settings.mcp_base_url,
    required_scopes=[settings.mcp_required_scope],
)

mcp = FastMCP(
    name="Room Booking MCP Server",
    auth=auth_provider,
)

register_room_tools(mcp)
register_booking_tools(mcp)
