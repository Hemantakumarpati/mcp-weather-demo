import asyncio
import sys
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

import os

async def run():
    # Define server parameters to run the server script directly
    # Use absolute path to ensure it works regardless of CWD
    server_script = os.path.join(os.path.dirname(os.path.abspath(__file__)), "weather_server.py")
    
    server_params = StdioServerParameters(
        command=sys.executable, # Use the same python interpreter
        args=[server_script],
        env=None # Inherit env
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # Initialize the connection
            await session.initialize()

            # List available tools
            tools = await session.list_tools()
            print("Connected to server.")
            print(f"Available tools: {[tool.name for tool in tools.tools]}")

            # Get city from CLI args or user input
            if len(sys.argv) > 1:
                city = sys.argv[1]
            else:
                city = input("\nEnter a city to check weather for: ")

            print(f"\nCalling get_weather for '{city}'...")
            result = await session.call_tool("get_weather", arguments={"city": city})
            print(f"Result: {result.content[0].text}")

if __name__ == "__main__":
    asyncio.run(run())
