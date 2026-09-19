from pydantic import BaseModel


class RouteInfo(BaseModel):
    route_number: int
    distance_miles: float
    duration_minutes: float


class RouteResponse(BaseModel):
    start: str
    destination: str
    fastest_route: RouteInfo
    eco_route: RouteInfo
    routes: list[RouteInfo]