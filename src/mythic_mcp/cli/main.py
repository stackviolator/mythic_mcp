"""Main CLI interface for Mythic MCP."""

import asyncio
import inspect
import os
from mcp.server.fastmcp import FastMCP
from mythic_mcp.api.mythic_api import MythicAPI
import mythic_mcp.tools.tools as tools
import mythic_mcp.prompts.templates as templates
from dotenv import load_dotenv

load_dotenv()

mcp = FastMCP("mythic_mcp")
api = None

def register_tools():
    """Automatically register all async functions from the tools module."""
    for name, func in inspect.getmembers(tools, inspect.isfunction):
        if inspect.iscoroutinefunction(func):
            async def wrapper(*args, **kwargs):
                return await func(api, *args, **kwargs)
            wrapper.__name__ = func.__name__
            wrapper.__doc__ = func.__doc__
            mcp.tool()(wrapper)

def register_prompts():
    """Automatically register all functions from the templates module as prompts."""
    for name, func in inspect.getmembers(templates, inspect.isfunction):
        mcp.prompt()(func)

def main():
    username = os.getenv("MYTHIC_API_USERNAME", "mythic_admin")
    password = os.getenv("MYTHIC_API_PASSWORD", "password")
    host = os.getenv("MYTHIC_API_HOST", "localhost")
    port = os.getenv("MYTHIC_API_PORT", "8000")

    api = MythicAPI(username, password, host, port)
    
    register_tools()
    register_prompts()
    asyncio.run(api.connect())
    
    mcp.settings.port = int(os.getenv("MYTHIC_MCP_PORT", "8888"))
    mcp.settings.host = os.getenv("MYTHIC_MCP_HOST", "0.0.0.0")
    
    print(f"Running MCP on {mcp.settings.host}:{mcp.settings.port}")
    mcp.run("sse")

if __name__ == "__main__":
    main()
