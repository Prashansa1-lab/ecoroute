from pydantic import BaseModel


class RouteInfo(BaseModel):
    route_number: int
    distance_miles: float
    duration_minutes: float
    scenic_score: int | None = None


class RouteResponse(BaseModel):
    start: str
    destination: str
    fastest_route: RouteInfo
    eco_route: RouteInfo
    scenic_route: RouteInfo | None
    routes: list[RouteInfo]