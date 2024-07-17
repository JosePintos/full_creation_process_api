from fastapi import APIRouter, HTTPException, Request, Query
from fastapi.params import Depends
from sqlalchemy.orm import Session
from ..db.schemas import Lead, LeadCreate, LeadReturn, NotFoundException
from ..db.connection import get_db
from typing import List, Annotated
from ..helpers.services import LeadService
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/leads")


@router.get("/")
def get_leads(
    request: Request,
    db: Session = Depends(get_db),
    limit: Annotated[
        int | None, Query(description="Número máximo de resultados a devolver")
    ] = 10,
    offset: Annotated[
        int | None, Query(description="Número de resultados a saltar desde el inicio")
    ] = 0,
) -> List[Lead]:
    """
    Obtiene todos los leads de la base de datos.

    Args:
        request (Request): El objeto de la solicitud.
        db (Session): La sesión de la base de datos, inyectada por FastAPI.

    Returns:
        List[Lead]: Una lista de objetos Lead.
    """
    lead_service = LeadService(db)
    try:
        leads = lead_service.read_all_leads(limit=limit, offset=offset)
    except NotFoundException as e:
        raise HTTPException(status_code=400, detail=e.message) from e
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
    try:
        db_lead = lead_service.read_lead(lead_id)
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=e.message) from e
    return db_lead


@router.post("/")
def add_lead(
    request: Request, lead_data: LeadCreate, db: Session = Depends(get_db)
) -> LeadReturn:
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
    logger.debug(f"{type(new_lead.lead_id)}")
    return LeadReturn(**new_lead.__dict__)
