from typing import Optional, List
from sqlalchemy import ForeignKey, ForeignKeyConstraint, UniqueConstraint
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

    cursados: Mapped[List["DBCursado"]] = relationship(
        "DBCursado", back_populates="lead"
    )


class DBCarrera(Base):
    __tablename__ = "carreras"

    carrera_id: Mapped[int] = mapped_column(primary_key=True, index=True)
    nombre: Mapped[str] = mapped_column(nullable=False)

    materias: Mapped[List["DBMateria"]] = relationship(
        "DBMateria", back_populates="carrera"
    )


class DBMateria(Base):
    __tablename__ = "materias"

    materia_id: Mapped[int] = mapped_column(primary_key=True, index=True)
    nombre: Mapped[str] = mapped_column(nullable=False)
    carrera_id: Mapped[int] = mapped_column(ForeignKey("carreras.id"))

    carrera: Mapped["DBCarrera"] = relationship("DBCarrera", back_populates="materias")


class DBCursado(Base):
    __tablename__ = "cursados"

    año_cursado: Mapped[int] = mapped_column(primary_key=True, index=True)
    carrera_id: Mapped[int] = mapped_column(primary_key=True, index=True)
    lead_id: Mapped[int] = mapped_column(primary_key=True, index=True)
    universidad: Mapped[Optional[str]]

    UniqueConstraint("carrera_id", "lead_id")

    lead: Mapped["DBLead"] = relationship("DBLead", back_populates="cursados")
    carrera: Mapped["DBCarrera"] = relationship("DBCarrera")
    inscripciones: Mapped[List["DBInscripcionMateria"]] = relationship(
        "DBInscripcionMateria", back_populates="cursados"
    )


class DBInscripcionMateria(Base):
    __tablename__ = "inscripcion_materia"

    año_cursado: Mapped[int] = mapped_column(primary_key=True, index=True)
    carrera_id: Mapped[int] = mapped_column(primary_key=True, index=True)
    lead_id: Mapped[int] = mapped_column(primary_key=True, index=True)
    materia_id: Mapped[int] = mapped_column(primary_key=True, index=True)
    veces_cursada: Mapped[int] = mapped_column(nullable=False)

    UniqueConstraint("carrera_id", "lead_id", "materia_id")

    materia: Mapped["DBMateria"] = relationship("DBMateria")
    carrera: Mapped["DBCarrera"] = relationship("DBCarrera")
    lead: Mapped["DBLead"] = relationship("DBLead")
