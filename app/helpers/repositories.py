from sqlalchemy.orm import Session
from sqlalchemy import select
from db.models import DBCarrera, DBCursado, DBInscripcionMateria, DBLead, DBMateria
import logging
from fastapi import HTTPException

logger = logging.getLogger(__name__)


class LeadRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def create_db_lead(self, db_lead: DBLead) -> DBLead:
        self.db.add(db_lead)
        self.db.commit()
        self.db.refresh(db_lead)
        return db_lead

    def read_all_db_leads(self) -> DBLead:
        return self.db.execute(select(DBLead)).scalars().all()

    def read_db_lead(self, lead_id: int) -> DBLead:
        db_lead = self.db.execute(
            select(DBLead).where(DBLead.lead_id == lead_id)
        ).scalar()
        if db_lead is None:
            raise HTTPException(
                status_code=404, detail=f"Lead with id {lead_id} not found."
            )
        return db_lead


class CarreraRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def create_db_carrera(self, db_carrera: DBCarrera) -> DBCarrera:
        # db_carrera = DBCarrera(**carrera.model_dump(exclude_none=True))
        self.db.add(db_carrera)
        self.db.commit()
        self.db.refresh(db_carrera)
        return db_carrera

    def read_all_db_carrera(self) -> DBCarrera:
        return self.db.execute(select(DBCarrera)).scalars().all()


class MateriaRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def create_materia(self, db_materia: DBMateria) -> DBMateria:
        # db_materia = DBMateria(**materia.model_dump(exclude_none=True))
        self.db.add(db_materia)
        self.db.commit()
        self.db.refresh(db_materia)
        return db_materia

    def read_materia(self) -> DBMateria:
        return self.db.execute(select(DBMateria)).scalars().all()


class CursadoRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def create_cursado(self, db_cursado: DBCursado) -> DBCursado:
        # db_cursado = DBCursado(**cursado.model_dump(exclude_none=True))
        self.db.add(db_cursado)
        self.db.commit()
        self.db.refresh(db_cursado)
        return db_cursado

    def read_cursado(self) -> DBCursado:
        return self.db.execute(select(DBCursado)).scalars().all()


class InscripcionMateriaRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def create_inscripcion_materia(
        self, db_insc: DBInscripcionMateria
    ) -> DBInscripcionMateria:
        # db_insc = DBInscripcionMateria(
        #     **inscripcion_materia.model_dump(exclude_none=True)
        # )
        self.db.add(db_insc)
        self.db.commit()
        self.db.refresh(db_insc)
        return db_insc

    def read_inscripcion_materia(self) -> DBMateria:
        return self.db.execute(select(DBInscripcionMateria)).scalars().all()
