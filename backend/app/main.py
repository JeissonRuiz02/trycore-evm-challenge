from fastapi import FastAPI

from app.api import api_router

app = FastAPI(title="Trycore EVM Tool API")
app.include_router(api_router)
