# python_entratus
Microservice FastAPI
# Async Weather Microservice

## 📌 Setup Instructions
1. Install dependencies:
pip install -r requirements.txt

2. Create `.env` file with your WeatherAPI key.

3. Start API using:
`uvicorn main:app --reload`
4. Fetch weather:
`GET /fetch_data/{location}`
5. Retrieve stored results:
`GET /results`
6. Run tests using:
`pytest test_script.py`
