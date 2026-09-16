from fastapi import FastAPI

app = FastAPI(
    title="EcoRoute API",
    description="Backend API for the EcoRoute travel route planner.",
    version="0.1.0",
)


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