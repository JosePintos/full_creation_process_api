from sqlalchemy.orm import Session
from sqlalchemy import select
from ..db.models import DBCarrera, DBCursado, DBInscripcionMateria, DBLead, DBMateria
from fastapi import Query
from ..db.schemas import NotFoundException


class LeadRepository:
    def __init__(self, db: Session) -> None:
        """
        Inicializa el repositorio con una sesión de base de datos.

        Args:
            db (Session): La sesión de la base de datos.
        """
        self.db = db

    def create_db_lead(self, db_lead: DBLead) -> DBLead:
        """
        Crea un nuevo lead en la base de datos.

        Args:
            db_lead (DBLead): El objeto DBLead a ser creado.

        Returns:
            DBLead: El objeto DBLead creado y guardado en la base de datos.
        """
        self.db.add(db_lead)
        self.db.commit()
        self.db.refresh(db_lead)
        return db_lead

    def read_all_db_leads(self, limit=Query, offset=Query) -> list[DBLead]:
        """
        Lee todos los leads de la base de datos.

        Args:
            limit (Query): Número máximo de resultados a devolver. Default 10
            offset (Query): Número de resultados a saltar desde el inicio. Default 0

        Returns:
            list[DBLead]: Lista de todos los objetos DBLead en la base de datos.
        """
        if not isinstance(limit, int) or not isinstance(offset, int):
            raise NotFoundException(f"Illegal limit/offset value. Only numbers >= 0.")
        if limit < 0 or offset < 0:
            raise NotFoundException(f"Illegal limit/offset value. Only numbers >= 0.")

        return (
            self.db.execute(select(DBLead).limit(limit).offset(offset)).scalars().all()
        )

    def read_db_lead(self, lead_id: int) -> DBLead:
        """
        Lee un lead específico de la base de datos usando su ID.

        Args:
            lead_id (int): El ID del lead a ser leído.

        Returns:
            DBLead: El objeto DBLead con el ID especificado.

        Raises:
            HTTPException: Si no se encuentra un lead con el ID proporcionado.
        """
        db_lead = self.db.execute(
            select(DBLead).where(DBLead.lead_id == lead_id)
        ).scalar()
        if db_lead is None:
            raise NotFoundException(f"Lead with id {lead_id} not found.")
        return db_lead


class CarreraRepository:
    def __init__(self, db: Session) -> None:
        """
        Inicializa el repositorio con una sesión de base de datos.

        Args:
            db (Session): La sesión de la base de datos.
        """
        self.db = db

    def read_or_create_carrera(self, carrera_nombre: str) -> DBCarrera:
        """
        Lee una carrera de la base de datos por su nombre o la crea si no existe.

        Args:
            carrera_nombre (str): El nombre de la carrera a ser leída o creada.

        Returns:
            DBCarrera: El objeto DBCarrera leído o creado.
        """
        db_carrera = self.db.execute(
            select(DBCarrera).where(DBCarrera.nombre == carrera_nombre)
        ).scalar()
        if db_carrera is None:
            db_carrera = DBCarrera(nombre=carrera_nombre)
            self.db.add(db_carrera)
            self.db.commit()
            self.db.refresh(db_carrera)
        return db_carrera


class MateriaRepository:
    def __init__(self, db: Session) -> None:
        """
        Inicializa el repositorio con una sesión de base de datos.

        Args:
            db (Session): La sesión de la base de datos.
        """
        self.db = db

    def read_or_create_materia(self, materia_nombre: str, carrera_id: int) -> DBMateria:
        """
        Lee una materia de la base de datos por su nombre o la crea si no existe.

        Args:
            materia_nombre (str): El nombre de la materia a ser leída o creada.
            carrera_id (int): El ID de la carrera asociada a la materia.

        Returns:
            DBMateria: El objeto DBMateria leído o creado.
        """
        db_materia = self.db.execute(
            select(DBMateria).where(DBMateria.nombre == materia_nombre)
        ).scalar()
        if db_materia is None:
            db_materia = DBMateria(nombre=materia_nombre, carrera_id=carrera_id)
            self.db.add(db_materia)
            self.db.commit()
            self.db.refresh(db_materia)
        return db_materia


class CursadoRepository:
    def __init__(self, db: Session) -> None:
        """
        Inicializa el repositorio con una sesión de base de datos.

        Args:
            db (Session): La sesión de la base de datos.
        """
        self.db = db

    def create_cursado(self, db_cursado: DBCursado) -> DBCursado:
        """
        Crea un nuevo cursado en la base de datos.

        Args:
            db_cursado (DBCursado): El objeto DBCursado a ser creado.

        Returns:
            DBCursado: El objeto DBCursado creado y guardado en la base de datos.
        """
        self.db.add(db_cursado)
        self.db.commit()
        self.db.refresh(db_cursado)
        return db_cursado

    def read_cursado(self) -> list[DBCursado]:
        """
        Lee todos los cursados de la base de datos.

        Returns:
            list[DBCursado]: Lista de todos los objetos DBCursado en la base de datos.
        """
        return self.db.execute(select(DBCursado)).scalars().all()


class InscripcionMateriaRepository:
    def __init__(self, db: Session) -> None:
        """
        Inicializa el repositorio con una sesión de base de datos.

        Args:
            db (Session): La sesión de la base de datos.
        """
        self.db = db

    def create_inscripcion_materia(
        self,
        db_inscripcion: DBInscripcionMateria,
    ) -> DBInscripcionMateria:
        """
        Crea una nueva inscripción de materia en la base de datos.

        Args:
            db_inscripcion (DBInscripcionMateria): El objeto DBInscripcionMateria a ser creado.

        Returns:
            DBInscripcionMateria: El objeto DBInscripcionMateria creado y guardado en la base de datos.
        """
        self.db.add(db_inscripcion)
        self.db.commit()
        self.db.refresh(db_inscripcion)
        return db_inscripcion

    def read_inscripcion_materia(self) -> list[DBMateria]:
        """
        Lee todas las inscripciones de materias de la base de datos.

        Returns:
            list[DBMateria]: Lista de todos los objetos DBInscripcionMateria en la base de datos.
        """
        return self.db.execute(select(DBInscripcionMateria)).scalars().all()
