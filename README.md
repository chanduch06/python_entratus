# Weather Microservice (Local)

## Overview
This microservice fetches weather data from an external API, processes the data, stores it in a SQLite database, and exposes endpoints to fetch and retrieve the processed data.

Key Features:
- Asynchronous API calls to fetch weather data.
- Data processing and storage using SQLite.
- REST API endpoints built with FastAPI.
- Containerized setup using Docker for simplified deployment.

## Setup Instructions

### Requirements
- Python 3.9+

### Install virtual environemnt
```bash
python -m venv venv
source venv/bin/activate   # For Linux/MacOS
venv\Scripts\activate      # For Windows
```


### Environment Variables
Create a `.env` file with your Weather API key:


### Running the Service Locally
1. Clone the repository.
2. Install dependencies: `pip install -r requirements.txt`.
3. Start the FastAPI server: `uvicorn main:app --reload`.
4. Access the API docs at `http://127.0.0.1:8000/docs`.

### Endpoints
1. `GET /fetch_data?city=<City_Name>`: Fetch weather data for a specific city and store it in SQLite.
2. `GET /results`: Retrieve stored weather data.

### Running Tests
Use `pytest` to run tests:
```bash
pytest test_main.py
```

# Weather Microservice (Docker Local Setup)

#

## Prerequisites
Before starting, ensure the following tools are installed:
- Docker: [Download Docker](https://www.docker.com/)

---

## **Setup Instructions**

### **1. build the docker image**
Start by cloning the repository:
```bash
docker-compose build
```

### **2. run the docker image**

```bash
docker-compose up
```

### **3. run the API**
Fetch weather data for a specific city using the /fetch_data endpoint:
```bash
curl "http://localhost:8000/fetch_data?city=Orlando"
```
Retrieve stored weather data using the /results endpoint:
```bash
curl "http://localhost:8000/results"
```

### **3.run tests in docker**
Run pytest inside the Docker container to validate the application:
```bash
docker-compose exec app pytest test_main.py
```

### **4.cleanup**
Stop and remove all containers:
```bash
docker-compose down
```

# Design Choices
- Async Programming: aiohttp for non-blocking API calls.
- Data Transformation: Pandas simplifies parsing and filtering.
- Database: SQLite for lightweight storage; SQLAlchemy for ORM.
- Framework: FastAPI for building modern, performant APIs.
- Containerization: Docker simplifies deployment and ensures consistency.
- Testing: pytest validates the functionality of API endpoints and data processing logic.


