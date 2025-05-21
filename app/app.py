from config import Config
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from router import router as api_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=Config.AllowOrigins,
    allow_methods=Config.AllowMethods,
    allow_headers=Config.AllowHeaders,
)

app.include_router(api_router)
