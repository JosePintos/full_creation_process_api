from typing import Optional, List
from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class DBLead(Base):
    __tablename__ = "leads"

    lead_id: Mapped[int] = mapped_column(primary_key=True, index=True)
    nombre: Mapped[str] = mapped_column(nullable=False)
    apellido: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[Optional[str]]
    direccion: Mapped[Optional[str]]
    tel: Mapped[Optional[int]]

    cursados: Mapped[List["DBCursado"]] = relationship(back_populates="lead")


class DBCarrera(Base):
    __tablename__ = "carreras"

    carrera_id: Mapped[int] = mapped_column(primary_key=True, index=True)
    nombre: Mapped[str] = mapped_column(nullable=False)


class DBMateria(Base):
    __tablename__ = "materias"

    materia_id: Mapped[int] = mapped_column(primary_key=True, index=True)
    nombre: Mapped[str] = mapped_column(nullable=False)
    carrera_id: Mapped[int] = mapped_column(ForeignKey("carreras.carrera_id"))


class DBCursado(Base):
    __tablename__ = "cursados"

    año_cursado: Mapped[int] = mapped_column(primary_key=True, index=True)
    carrera_id: Mapped[int] = mapped_column(
        ForeignKey("carreras.carrera_id"), primary_key=True, index=True
    )
    lead_id: Mapped[int] = mapped_column(
        ForeignKey("leads.lead_id"), primary_key=True, index=True
    )
    universidad: Mapped[Optional[str]]

    lead: Mapped["DBLead"] = relationship("DBLead", back_populates="cursados")
    carrera: Mapped["DBCarrera"] = relationship("DBCarrera")
    inscripciones: Mapped[List["DBInscripcionMateria"]] = relationship(
        "DBInscripcionMateria",
        back_populates="cursado",
        primaryjoin="and_(DBCursado.año_cursado==DBInscripcionMateria.año_cursado, DBCursado.carrera_id==DBInscripcionMateria.carrera_id, DBCursado.lead_id==DBInscripcionMateria.lead_id)",
    )


class DBInscripcionMateria(Base):
    __tablename__ = "inscripcion_materia"

    año_cursado: Mapped[int] = mapped_column(
        ForeignKey("cursados.año_cursado"), primary_key=True, index=True
    )
    carrera_id: Mapped[int] = mapped_column(
        ForeignKey("cursados.carrera_id"), primary_key=True, index=True
    )
    lead_id: Mapped[int] = mapped_column(
        ForeignKey("cursados.lead_id"), primary_key=True, index=True
    )
    materia_id: Mapped[int] = mapped_column(
        ForeignKey("materias.materia_id"), primary_key=True, index=True
    )
    veces_cursada: Mapped[int]

    cursado: Mapped["DBCursado"] = relationship(
        "DBCursado",
        back_populates="inscripciones",
        primaryjoin="and_(DBInscripcionMateria.año_cursado==DBCursado.año_cursado, DBInscripcionMateria.carrera_id==DBCursado.carrera_id, DBInscripcionMateria.lead_id==DBCursado.lead_id)",
    )
    materia: Mapped["DBMateria"] = relationship("DBMateria", foreign_keys=[materia_id])

    __table_args__ = (
        UniqueConstraint("año_cursado", "carrera_id", "lead_id", name="uq_inscripcion"),
    )
