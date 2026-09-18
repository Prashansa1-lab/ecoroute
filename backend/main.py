from fastapi import FastAPI
import requests

app = FastAPI(
    title="EcoRoute API",
    description="Backend API for the EcoRoute travel route planner.",
    version="0.1.0",
)
def geocode_location(location: str):
    url = "https://nominatim.openstreetmap.org/search"

    params = {
        "q": location,
        "format": "json",
        "limit": 1
    }

    headers = {
        "User-Agent": "EcoRoute/0.1"
    }

    response = requests.get(url, params=params, headers=headers)
    response.raise_for_status()

    data = response.json()

    if not data:
        return None

    return {
        "latitude": float(data[0]["lat"]),
        "longitude": float(data[0]["lon"])
    }
@app.get("/geocode")
def geocode(location: str):
    coordinates = geocode_location(location)

    return {
        "location": location,
        "coordinates": coordinates
    }


@app.get("/")
def home():
    return {
        "message": "EcoRoute API is running",
        "status": "healthy"
    }
@app.get("/routes")
def get_routes(start: str, destination: str):
    return {
        "start": start,
        "destination": destination,
        "routes": [
            {
                "name": "Fastest",
                "distance_miles": 31.2,
                "duration_minutes": 37,
                "eco_score": 68
            },
            {
                "name": "Eco",
                "distance_miles": 29.8,
                "duration_minutes": 42,
                "eco_score": 87
            },
            {
                "name": "Scenic",
                "distance_miles": 34.1,
                "duration_minutes": 48,
                "eco_score": 81
            }
        ]
    }