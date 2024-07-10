from fastapi import FastAPI, HTTPException, APIRouter
from pydantic import BaseModel
from routers.leads import router as leads_router

app = FastAPI()

app.include_router(leads_router)


@app.get("/")
def start_server():
    return "Server is running."
