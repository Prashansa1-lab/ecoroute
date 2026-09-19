import os
import requests
from dotenv import load_dotenv

load_dotenv()

ORS_API_KEY = os.getenv("ORS_API_KEY")


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
        ],
        "alternative_routes": {
            "target_count": 3,
            "weight_factor": 1.6,
            "share_factor": 0.6
        }
    }

    response = requests.post(url, json=body, headers=headers)
    response.raise_for_status()

    return response.json()