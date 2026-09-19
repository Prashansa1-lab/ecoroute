from fastapi import FastAPI
from routes.routes import router

app = FastAPI(
    title="EcoRoute API",
    description="Backend API for the EcoRoute travel route planner.",
    version="0.1.0",
)

app.include_router(router)


@app.get("/")
def home():
    return {
        "message": "EcoRoute API is running",
        "status": "healthy"
    }