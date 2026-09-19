from fastapi import APIRouter, HTTPException

from models.route import RouteResponse
from services.geocoding import geocode_location
from services.routing import get_driving_route
from services.route_scoring import find_fastest_route, find_eco_route
from services.scenic import analyze_route_scenery


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


@router.get("/routes", response_model=RouteResponse)
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

    route_data = get_driving_route(
        start_coords,
        destination_coords
    )

    routes = []

    for index, route in enumerate(route_data["routes"]):
        summary = route["summary"]

        distance_miles = summary["distance"] / 1609.344
        duration_minutes = summary["duration"] / 60

        scenic_score = analyze_route_scenery(
            route["geometry"]
        )

        routes.append({
            "route_number": index + 1,
            "distance_miles": round(distance_miles, 1),
            "duration_minutes": round(duration_minutes, 1),
            "scenic_score": scenic_score
        })

    fastest_route = find_fastest_route(routes)
    eco_route = find_eco_route(routes)

    routes_with_scenic_data = [
        route
        for route in routes
        if route["scenic_score"] is not None
    ]

    scenic_route = (
        max(
            routes_with_scenic_data,
            key=lambda route: route["scenic_score"]
        )
        if routes_with_scenic_data
        else None
    )

    return {
        "start": start,
        "destination": destination,
        "fastest_route": fastest_route,
        "eco_route": eco_route,
        "scenic_route": scenic_route,
        "routes": routes
    }