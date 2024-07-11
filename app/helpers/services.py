from .repositories import (
    LeadRepository,
    CarreraRepository,
    InscripcionMateriaRepository,
    CursadoRepository,
    MateriaRepository,
)
from sqlalchemy.orm import Session
from db.models import DBCarrera, DBCursado, DBInscripcionMateria, DBLead, DBMateria
from db.schemas import Lead, LeadCreate
import logging

logger = logging.getLogger(__name__)


class LeadService:
    def __init__(self, db: Session) -> None:
        self.lead_repository = LeadRepository(db)
        self.carrera_repository = CarreraRepository(db)
        self.materia_repository = MateriaRepository(db)
        self.cursado_repository = CursadoRepository(db)
        self.inscripcion_materia_repository = InscripcionMateriaRepository(db)

    def create_lead(self, lead: Lead) -> DBLead:
        # db_lead = DBLead(**lead.model_dump(exclude_none=True))
        db_lead = DBLead(
            nombre=lead.nombre,
            apellido=lead.apellido,
            email=lead.email,
            direccion=lead.direccion,
            tel=lead.tel,
        )
        created_lead = self.lead_repository.create_db_lead(db_lead)
        # create and add cursado with carrera and materias
        for cursado in lead.cursados:
            db_cursado = DBCursado(
                año_cursado=cursado.año_cursado,
                carrera_id=cursado.carrera_id,
                lead_id=created_lead.lead_id,
                universidad=cursado.universidad,
            )
            self.cursado_repository.create_cursado(db_cursado)

            for inscripcion in cursado.inscripciones:
                db_materia = DBInscripcionMateria(
                    año_cursado=cursado.año_cursado,
                    carrera_id=cursado.carrera_id,
                    lead_id=created_lead.lead_id,
                    materia_id=inscripcion.materia_id,
                    veces_cursada=inscripcion.veces_cursada,
                )

    def read_all_leads(self) -> Lead:
        return self.lead_repository.read_all_db_leads()

    def read_lead(self, lead_id: int) -> Lead:
        return self.lead_repository.read_db_lead(lead_id)
