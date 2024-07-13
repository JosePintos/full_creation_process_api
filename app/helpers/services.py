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


class LeadService:
    def __init__(self, db: Session) -> None:
        """
        Inicializa el servicio con los repositorios necesarios.

        Args:
            db (Session): La sesión de la base de datos.
        """
        self.lead_repository = LeadRepository(db)
        self.carrera_repository = CarreraRepository(db)
        self.materia_repository = MateriaRepository(db)
        self.cursado_repository = CursadoRepository(db)
        self.inscripcion_materia_repository = InscripcionMateriaRepository(db)

    def create_lead(self, lead: LeadCreate) -> DBLead:
        """
        Crea un nuevo lead en la base de datos y agrega sus cursados e inscripciones si existen.

        Args:
            lead (LeadCreate): Los datos del lead a ser creado.

        Returns:
            DBLead: El objeto DBLead creado y guardado en la base de datos.
        """
        db_lead = self.lead_repository.create_db_lead(
            DBLead(
                nombre=lead.nombre,
                apellido=lead.apellido,
                email=lead.email,
                direccion=lead.direccion,
                tel=lead.tel,
            )
        )
        # Agregar cursados con carrera y materias
        if len(lead.cursados) > 0:
            for cursado in lead.cursados:
                self.add_cursado(db_lead.lead_id, cursado)
        return db_lead

    def add_cursado(self, lead_id: int, cursado: CursadoCreate) -> DBCursado:
        """
        Agrega un nuevo cursado para un lead específico.

        Args:
            lead_id (int): El ID del lead.
            cursado (CursadoCreate): Los datos del cursado a ser agregado.

        Returns:
            DBCursado: El objeto DBCursado creado y guardado en la base de datos.
        """
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
        """
        Agrega una nueva inscripción de materia para un lead específico.

        Args:
            lead_id (int): El ID del lead.
            materia_id (int): El ID de la materia.
            carrera_id (int): El ID de la carrera.
            año_cursado (int): El año de cursado.
            inscripcion (InscripcionMateriaCreate): Los datos de la inscripción a ser agregada.

        Returns:
            DBInscripcionMateria: El objeto DBInscripcionMateria creado y guardado en la base de datos.
        """
        return self.inscripcion_materia_repository.create_inscripcion_materia(
            DBInscripcionMateria(
                año_cursado=año_cursado,
                carrera_id=carrera_id,
                lead_id=lead_id,
                materia_id=materia_id,
                veces_cursada=inscripcion.veces_cursada,
            )
        )

    def read_all_leads(self) -> list[DBLead]:
        """
        Lee todos los leads de la base de datos.

        Returns:
            list[DBLead]: Lista de todos los objetos DBLead en la base de datos.
        """
        return self.lead_repository.read_all_db_leads()

    def read_lead(self, lead_id: int) -> DBLead:
        """
        Lee un lead específico de la base de datos usando su ID.

        Args:
            lead_id (int): El ID del lead a ser leído.

        Returns:
            DBLead: El objeto DBLead con el ID especificado.
        """
        return self.lead_repository.read_db_lead(lead_id)
