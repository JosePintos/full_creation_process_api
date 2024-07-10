from typing import Optional
from sqlalchemy import ForeignKey, ForeignKeyConstraint
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class DBLead(Base):
    __tablename__ = "leads"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    nombre: Mapped[str]
    apellido: Mapped[str]
    email: Mapped[Optional[str]]
    tel: Mapped[Optional[int]]


class DBCarrera(Base):
    __tablename__ = "carreras"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    nombre: Mapped[str]


class DBMateria(Base):
    __tablename__ = "materias"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    nombre: Mapped[str]
    carrera_id: Mapped[int] = mapped_column(ForeignKey("carreras.id"))


class DBCursado(Base):
    __tablename__ = "cursados"

    año_cursado: Mapped[int] = mapped_column(primary_key=True, index=True)
    carrera_id: Mapped[int] = mapped_column(primary_key=True, index=True)
    lead_id: Mapped[int] = mapped_column(primary_key=True, index=True)
    universidad: Mapped[Optional[str]]

    __table_args__ = (
        ForeignKeyConstraint(["carrera_id", "lead_id"], ["carreras.id", "leads.id"]),
    )


class DBInscripcionMateria(Base):
    __tablename__ = "inscripcion_materia"

    año_cursado: Mapped[int] = mapped_column(primary_key=True, index=True)
    carrera_id: Mapped[int] = mapped_column(primary_key=True, index=True)
    lead_id: Mapped[int] = mapped_column(primary_key=True, index=True)
    materia_id: Mapped[int] = mapped_column(primary_key=True, index=True)
    veces_cursada: Mapped[int]

    __table_args__ = (
        ForeignKeyConstraint(
            ["carrera_id", "lead_id", "materia_id"],
            ["carreras.id", "leads.id", "materias.id"],
        ),
    )
