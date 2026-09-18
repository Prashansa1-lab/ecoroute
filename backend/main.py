from fastapi import FastAPI
import requests
import os
from dotenv import load_dotenv

load_dotenv()

ORS_API_KEY = os.getenv("ORS_API_KEY")
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
def get_driving_route(start_coords, destination_coords):
    url = "https://api.heigit.org/openrouteservice/v2/directions/driving-car"

    headers = {
        "Authorization": ORS_API_KEY,
        "Content-Type": "application/json"
    }

    body = {
        "coordinates": [
            [
                start_coords["longitude"],
                start_coords["latitude"]
            ],
            [
                destination_coords["longitude"],
                destination_coords["latitude"]
            ]
        ]
    }

    response = requests.post(url, json=body, headers=headers)
    response.raise_for_status()

    return response.json()
@app.get("/test-route")
def test_route(start: str, destination: str):
    start_coords = geocode_location(start)
    destination_coords = geocode_location(destination)

    route_data = get_driving_route(start_coords, destination_coords)

    summary = route_data["routes"][0]["summary"]

    distance_miles = summary["distance"] / 1609.344
    duration_minutes = summary["duration"] / 60

    return {
        "start": start,
        "destination": destination,
        "distance_miles": round(distance_miles, 1),
        "duration_minutes": round(duration_minutes, 1)
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