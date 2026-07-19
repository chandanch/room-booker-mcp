from fastmcp import FastMCP
from fastmcp.server.auth.providers.azure import AzureProvider

from app.auth.context import get_current_user
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


@mcp.tool
def who_am_i() -> dict:
    user = get_current_user()

    return {
        "user_id": user.user_id,
        "name": user.name,
        "email": user.email,
        "tenant_id": user.tenant_id,
        "entra_roles": sorted(user.roles),
        "effective_permissions": sorted(user.permissions),
    }


def main() -> None:
    mcp.run(
        transport="http",
        host=settings.server_host,
        port=settings.server_port,
    )


if __name__ == "__main__":
    main()
