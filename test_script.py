import pytest
import asyncio
import aiohttp
from sqlalchemy import create_engine
import pandas as pd
from main import fetch_weather


def test_fetch_weather():
    """Test fetching weather data"""

    async def async_test():
        data = await fetch_weather(aiohttp.ClientSession(), "New York")
        assert data is not None
        assert "current" in data
        assert isinstance(data["current"]["temp_c"], (int, float))

    asyncio.run(async_test())


