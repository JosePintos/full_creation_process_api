from sqlalchemy.orm import Session
from sqlalchemy import select
from db.models import DBCarrera, DBCursado, DBInscripcionMateria, DBLead, DBMateria
from fastapi import HTTPException


import logging

logger = logging.getLogger(__name__)


class LeadRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def create_db_lead(self, db_lead: DBLead) -> DBLead:
        logger.debug(f"debug: {db_lead}")
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

    def read_or_create_carrera(self, carrera_nombre: str) -> DBCarrera:
        db_carrera = self.db.execute(
            select(DBCarrera).where(DBCarrera.nombre == carrera_nombre)
        ).scalar()
        logger.debug(f"carrera: {db_carrera}")
        if not db_carrera:
            db_carrera = DBCarrera(nombre=carrera_nombre)
            self.db.add(db_carrera)
            self.db.commit()
            self.db.refresh(db_carrera)
        return db_carrera


class MateriaRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def read_or_create_materia(self, materia_nombre: str) -> DBMateria:
        db_materia = self.db.execute(
            select(DBMateria).where(DBMateria.nombre == materia_nombre)
        ).scalar()
        if not db_materia:
            db_materia = DBMateria(nombre=materia_nombre)
            self.db.add(db_materia)
            self.db.commit()
            self.db.refresh(db_materia)
        return db_materia


class CursadoRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def create_cursado(self, db_cursado: DBCursado) -> DBCursado:
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
        self,
        db_inscripcion: DBInscripcionMateria,
    ) -> DBInscripcionMateria:
        self.db.add(db_inscripcion)
        self.db.commit()
        self.db.refresh(db_inscripcion)
        return db_inscripcion

    def read_inscripcion_materia(self) -> DBMateria:
        return self.db.execute(select(DBInscripcionMateria)).scalars().all()
