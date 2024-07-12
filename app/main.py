from fastapi import FastAPI
from app.routers.leads import router as leads_router

import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = FastAPI()

app.include_router(leads_router)


@app.get("/")
def start_server():
    return "Server is running."
