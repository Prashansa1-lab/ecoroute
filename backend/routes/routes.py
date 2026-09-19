from fastapi import APIRouter, HTTPException
from services.geocoding import geocode_location
from services.routing import get_driving_route
from services.route_scoring import find_fastest_route, find_eco_route

router = APIRouter()


@router.get("/geocode")
def geocode(location: str):
    coordinates = geocode_location(location)

    if coordinates is None:
        raise HTTPException(
            status_code=404,
            detail=f"Could not find location: {location}"
        )

    return {
        "location": location,
        "coordinates": coordinates
    }


@router.get("/routes")
def get_routes(start: str, destination: str):
    start_coords = geocode_location(start)
    destination_coords = geocode_location(destination)

    if start_coords is None:
        raise HTTPException(
            status_code=404,
            detail=f"Could not find start location: {start}"
        )

    if destination_coords is None:
        raise HTTPException(
            status_code=404,
            detail=f"Could not find destination: {destination}"
        )

    route_data = get_driving_route(start_coords, destination_coords)

    routes = []

    for index, route in enumerate(route_data["routes"]):
        summary = route["summary"]

        distance_miles = summary["distance"] / 1609.344
        duration_minutes = summary["duration"] / 60

        routes.append({
            "route_number": index + 1,
            "distance_miles": round(distance_miles, 1),
            "duration_minutes": round(duration_minutes, 1)
        })

    fastest_route = find_fastest_route(routes)
    eco_route = find_eco_route(routes)

    return {
    "start": start,
    "destination": destination,
    "fastest_route": fastest_route,
    "eco_route": eco_route,
    "routes": routes
}