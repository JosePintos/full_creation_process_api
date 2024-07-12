from fastapi import APIRouter, HTTPException, Request
from fastapi.params import Depends
from sqlalchemy.orm import Session
from db.schemas import Lead, LeadCreate
from db.connection import get_db
from typing import List
from helpers.services import LeadService

router = APIRouter(prefix="/leads")


@router.get("/")
def get_leads(request: Request, db: Session = Depends(get_db)) -> List[Lead]:
    """
    Obtiene todos los leads de la base de datos.

    Args:
        request (Request): El objeto de la solicitud.
        db (Session): La sesión de la base de datos, inyectada por FastAPI.

    Returns:
        List[Lead]: Una lista de objetos Lead.
    """
    lead_service = LeadService(db)
    leads = lead_service.read_all_leads()
    return leads


@router.get("/{lead_id}")
def get_lead(request: Request, lead_id: int, db: Session = Depends(get_db)) -> Lead:
    """
    Obtiene un lead específico por su ID.

    Args:
        request (Request): El objeto de la solicitud.
        lead_id (int): El ID del lead a obtener.
        db (Session): La sesión de la base de datos, inyectada por FastAPI.

    Returns:
        Lead: El objeto Lead con el ID especificado.
    """
    lead_service = LeadService(db)
    return lead_service.read_lead(lead_id)


@router.post("/")
def add_lead(
    request: Request, lead_data: LeadCreate, db: Session = Depends(get_db)
) -> Lead:
    """
    Agrega un nuevo lead a la base de datos.

    Args:
        request (Request): El objeto de la solicitud.
        lead_data (LeadCreate): Los datos del lead a ser creado.
        db (Session): La sesión de la base de datos, inyectada por FastAPI.

    Returns:
        Lead: El objeto Lead creado.

    Raises:
        HTTPException: Si ocurre un error al crear el lead.
    """
    lead_service = LeadService(db)
    try:
        new_lead = lead_service.create_lead(lead_data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    return new_lead
