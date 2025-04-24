import aiohttp
import asyncio
from fastapi import FastAPI
from dotenv import load_dotenv
import os
import pandas as pd
from sqlalchemy import create_engine
load_dotenv()
API_KEY = os.getenv("WEATHER_API_KEY")
BASE_URL = "http://api.weatherapi.com/v1/current.json"

# async def fetch_weather(session, location):
#     """Fetch weather data asynchronously from WeatherAPI"""
#     url = f"{BASE_URL}?key={API_KEY}&q={location}"
#     async with session.get(url) as response:
#         return await response.json() if response.status == 200 else None
#
# async def fetch_multiple_cities(cities):
#     """Fetch weather for multiple cities concurrently"""
#     async with aiohttp.ClientSession() as session:
#         tasks = [fetch_weather(session, city) for city in cities]
#         return await asyncio.gather(*tasks)
#


async def fetch_weather(location):
    async with aiohttp.ClientSession() as session:
        url = f"{BASE_URL}?key={API_KEY}&q={location}"
        async with session.get(url) as response:
            data = await response.json()
            return data if response.status == 200 else None


# async def main():
#     location = "New York"
#     weather_data = await fetch_weather(location)
#
#     if weather_data:
#         print("Raw API Response:", weather_data)  # Print entire API data
#         print("Temperature:", weather_data["current"]["temp_c"])  # Print specific field
#         print("Condition:", weather_data["current"]["condition"]["text"])
#     else:
#         print("Error: Failed to retrieve weather data")

#Run the async function
#asyncio.run(main())


# process and store the data



def process_and_store(data):
    if not data: return

    location = data["location"]["name"]
    temp = data["current"]["temp_c"]
    condition = data["current"]["condition"]["text"]

    df = pd.DataFrame([[location, temp, condition]], columns=["Location", "Temp_C", "Condition"])

    engine = create_engine("sqlite:///weather.db")
    df.to_sql("weather", engine, if_exists="replace", index=False)


# Build FastAPI endpoints



app = FastAPI()

@app.get("/fetch_data/{location}")
async def fetch_data(location: str):
    data = await fetch_weather(location)
    if data:
        process_and_store(data)
        return {"message": f"Weather data for {location} stored"}
    return {"error": "Failed to retrieve data"}

@app.get("/results")
def get_results():
    engine = create_engine("sqlite:///weather.db")
    df = pd.read_sql("SELECT * FROM weather", engine)
    return df.to_dict(orient="records")

