import asyncio

from fastmcp import Client

MCP_URL = "http://localhost:8000/mcp"


async def main() -> None:
    async with Client(
        MCP_URL,
        auth="oauth",
    ) as client:
        print("Authenticated with Microsoft Entra ID")

        identity = await client.call_tool(
            "who_am_i",
            {},
        )
        print(identity)

        rooms = await client.call_tool(
            "search_rooms",
            {
                "location": "BLR",
                "min_capacity": 2,
            },
        )
        print(rooms)


if __name__ == "__main__":
    asyncio.run(main())
