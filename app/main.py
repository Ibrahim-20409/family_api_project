from fastapi import FastAPI
from app.routes import router

app = FastAPI(
    title="Family Management API by SHAHMEER",
    description="An API for managing families and their members using CSV files.",
    version="1.0.0"
)

app.include_router(router)