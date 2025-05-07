"""Pytest configuration file."""

import pytest
import pytest_asyncio
from mythic_mcp.api.mythic_api import MythicAPI


@pytest_asyncio.fixture
async def mythic_api():
    """Create a MythicAPI instance for testing."""
    api = MythicAPI(
        username="test_user",
        password="test_pass",
        server_ip="127.0.0.1",
        server_port=7443,
    )
    return api
