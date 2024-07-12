from .repositories import (
    LeadRepository,
    CarreraRepository,
    InscripcionMateriaRepository,
    CursadoRepository,
    MateriaRepository,
)
from sqlalchemy.orm import Session
from ..db.models import DBCursado, DBInscripcionMateria, DBLead
from ..db.schemas import Lead, LeadCreate, InscripcionMateriaCreate, CursadoCreate
import logging

logger = logging.getLogger(__name__)


class LeadService:
    def __init__(self, db: Session) -> None:
        self.lead_repository = LeadRepository(db)
        self.carrera_repository = CarreraRepository(db)
        self.materia_repository = MateriaRepository(db)
        self.cursado_repository = CursadoRepository(db)
        self.inscripcion_materia_repository = InscripcionMateriaRepository(db)

    def create_lead(self, lead: LeadCreate) -> DBLead:
        db_lead = self.lead_repository.create_db_lead(
            DBLead(
                nombre=lead.nombre,
                apellido=lead.apellido,
                email=lead.email,
                direccion=lead.direccion,
                tel=lead.tel,
            )
        )
        # add cursados with carrera and materias
        for cursado in lead.cursados:
            self.add_cursado(db_lead.lead_id, cursado)
        return db_lead.lead_id

    def add_cursado(self, lead_id: int, cursado: CursadoCreate) -> DBCursado:
        db_carrera = self.carrera_repository.read_or_create_carrera(
            cursado.carrera.nombre
        )
        db_cursado = self.cursado_repository.create_cursado(
            DBCursado(
                año_cursado=cursado.año_cursado,
                carrera_id=db_carrera.carrera_id,
                lead_id=lead_id,
                universidad=cursado.universidad,
            )
        )
        for inscripcion in cursado.inscripciones:
            db_materia = self.materia_repository.read_or_create_materia(
                inscripcion.materia.nombre, db_carrera.carrera_id
            )
            self.add_inscripcion_materia(
                lead_id,
                db_materia.materia_id,
                db_carrera.carrera_id,
                db_cursado.año_cursado,
                inscripcion,
            )
        return db_cursado

    def add_inscripcion_materia(
        self,
        lead_id: int,
        materia_id: int,
        carrera_id: int,
        año_cursado: int,
        inscripcion: InscripcionMateriaCreate,
    ) -> DBInscripcionMateria:
        return self.inscripcion_materia_repository.create_inscripcion_materia(
            DBInscripcionMateria(
                año_cursado=año_cursado,
                carrera_id=carrera_id,
                lead_id=lead_id,
                materia_id=materia_id,
                veces_cursada=inscripcion.veces_cursada,
            )
        )

    def read_all_leads(self) -> Lead:
        return self.lead_repository.read_all_db_leads()

    def read_lead(self, lead_id: int) -> Lead:
        return self.lead_repository.read_db_lead(lead_id)
