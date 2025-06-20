from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from app.routes import router
from app.auth import authenticate_user, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES, Token

app = FastAPI(
    title="Family Management API by SHAHMEER",
    description="An API for managing families and their members using CSV files.",
    version="1.0.0"
)



# Protected routes
app.include_router(router)
