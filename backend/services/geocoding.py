import requests


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