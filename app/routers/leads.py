from fastapi import APIRouter, HTTPException, Request
from fastapi.params import Depends
from sqlalchemy.orm import Session
from ..db.schemas import Lead, LeadCreate
from ..db.connection import get_db
from typing import List
from ..helpers.services import LeadService
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/leads")


@router.get("/")
def get_leads(request: Request, db: Session = Depends(get_db)) -> List[Lead]:
    lead_service = LeadService(db)
    leads = lead_service.read_all_leads()
    return leads


@router.get("/{lead_id}")
def get_lead(request: Request, lead_id: int, db: Session = Depends(get_db)) -> Lead:
    lead_service = LeadService(db)
    return lead_service.read_lead(lead_id)


@router.post("/")
def add_lead(
    request: Request, lead_data: LeadCreate, db: Session = Depends(get_db)
) -> Lead:
    lead_service = LeadService(db)
    try:
        new_lead = lead_service.create_lead(lead_data)
        logger.debug(f"debug: {new_lead}")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    return new_lead
