import aiohttp
from fastapi import FastAPI, HTTPException
import pandas as pd
from sqlalchemy import create_engine, Column, String, Float
from sqlalchemy.orm import sessionmaker,  declarative_base
from dotenv import load_dotenv
import os

load_dotenv()
API_KEY = os.getenv("WEATHER_API_KEY")
BASE_URL = "http://api.weatherapi.com/v1/current.json"

# FastAPI instance
app = FastAPI()

# Define Base correctly
Base = declarative_base()

# ORM Model
class Weather(Base):
    __tablename__ = "weather"
    city = Column(String, primary_key=True)
    temperature = Column(Float)
    condition = Column(String)

# Database setup
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)
Base.metadata.create_all(engine)
SessionLocal = sessionmaker(bind=engine)


# Fetch data from external API
async def fetch_weather_data(city: str):
    async with aiohttp.ClientSession() as session:
        try:
            WEATHER_API_URL = f"{BASE_URL}?key={API_KEY}&q={city}" # External API URL
            async with session.get(WEATHER_API_URL.format(city=city)) as response:
                if response.status != 200:
                    raise HTTPException(status_code=response.status, detail="Failed to fetch weather data")
                return await response.json()
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

# Process data and store it
def process_and_store_data(data):
    df = pd.DataFrame([{
        "city": data["location"]["name"],
        "temperature": data["current"]["temp_f"],
        "condition" : data["current"]["condition"]["text"],

    }])

    session = SessionLocal()
    for _, row in df.iterrows():
        weather = Weather(city=row["city"], temperature=row["temperature"], condition=row["condition"])
        session.merge(weather)  # Update or insert
    session.commit()
    session.close()

# Routes
@app.get("/fetch_data")
async def fetch_data(city: str = "London"):
    weather_data = await fetch_weather_data(city)
    process_and_store_data(weather_data)
    return {"detail": f"Weather data for {city} fetched and stored successfully"}

@app.get("/results")
def get_results():
    session = SessionLocal()
    results = session.query(Weather).all()
    session.close()
    return [{"city": r.city, "temperature": r.temperature, "condition": r.condition} for r in results]

