from typing import Optional, List
from sqlalchemy import (
    ForeignKey,
    ForeignKeyConstraint,
    PrimaryKeyConstraint,
    UniqueConstraint,
    String,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.ext.associationproxy import AssociationProxy, association_proxy


class Base(DeclarativeBase):
    pass


class DBLead(Base):
    __tablename__ = "leads"

    lead_id: Mapped[int] = mapped_column(primary_key=True, index=True)
    nombre: Mapped[str] = mapped_column(String(50), nullable=False)
    apellido: Mapped[str] = mapped_column(String(50), nullable=False)
    email: Mapped[Optional[str]] = mapped_column(String(50))
    direccion: Mapped[Optional[str]] = mapped_column(String(100))
    tel: Mapped[Optional[int]] = mapped_column(String(50))

    cursados: Mapped[List["DBCursado"]] = relationship(
        "DBCursado", back_populates="lead"
    )


class DBCarrera(Base):
    __tablename__ = "carreras"

    carrera_id: Mapped[int] = mapped_column(primary_key=True, index=True)
    nombre: Mapped[str] = mapped_column(String(50), nullable=False)

    materias: Mapped[List["DBMateria"]] = relationship(
        "DBMateria", back_populates="carrera"
    )

    def __repr__(self) -> str:
        return f"<DBCarrera(carrera_id={self.carrera_id}, nombre={self.nombre})>"


class DBMateria(Base):
    __tablename__ = "materias"

    materia_id: Mapped[int] = mapped_column(primary_key=True, index=True)
    nombre: Mapped[str] = mapped_column(String(50), nullable=False)
    carrera_id: Mapped[int] = mapped_column(ForeignKey("carreras.carrera_id"))

    carrera: Mapped[DBCarrera] = relationship("DBCarrera", back_populates="materias")

    inscripciones: Mapped[List["DBInscripcionMateria"]] = relationship(
        "DBInscripcionMateria", back_populates="materia"
    )
    cursados: AssociationProxy[List["DBCursado"]] = association_proxy(
        "inscripciones", "materia"
    )

    def __repr__(self) -> str:
        return f"<DBMateria(materia_id={self.materia_id}, nombre={self.nombre}, carrera_id={self.carrera_id})>"


class DBCursado(Base):
    __tablename__ = "cursados"

    año_cursado: Mapped[int] = mapped_column(primary_key=True, index=True)
    carrera_id: Mapped[int] = mapped_column(
        ForeignKey("carreras.carrera_id"), primary_key=True, index=True
    )
    lead_id: Mapped[int] = mapped_column(
        ForeignKey("leads.lead_id"), primary_key=True, index=True
    )
    universidad: Mapped[Optional[str]] = mapped_column(String(100))

    lead: Mapped["DBLead"] = relationship("DBLead", back_populates="cursados")
    carrera: Mapped["DBCarrera"] = relationship("DBCarrera")

    inscripciones: Mapped[List["DBInscripcionMateria"]] = relationship(
        "DBInscripcionMateria",
        back_populates="cursado",
        primaryjoin="and_(DBInscripcionMateria.año_cursado == DBCursado.año_cursado, "
        "DBInscripcionMateria.carrera_id == DBCursado.carrera_id,"
        "DBInscripcionMateria.lead_id == DBCursado.lead_id)",
    )
    materias: AssociationProxy[List["DBMateria"]] = association_proxy(
        "inscripciones", "cursado"
    )

    __table_args__ = (PrimaryKeyConstraint("año_cursado", "carrera_id", "lead_id"),)


class DBInscripcionMateria(Base):
    __tablename__ = "inscripcion_materia"

    año_cursado: Mapped[int] = mapped_column(primary_key=True, index=True)
    carrera_id: Mapped[int] = mapped_column(primary_key=True, index=True)
    lead_id: Mapped[int] = mapped_column(primary_key=True, index=True)
    materia_id: Mapped[int] = mapped_column(
        ForeignKey("materias.materia_id"), primary_key=True, index=True
    )
    veces_cursada: Mapped[int]

    cursado: Mapped["DBCursado"] = relationship(
        "DBCursado",
        back_populates="inscripciones",
    )
    materia: Mapped["DBMateria"] = relationship(
        "DBMateria", back_populates="inscripciones"
    )

    __table_args__ = (
        PrimaryKeyConstraint("año_cursado", "carrera_id", "lead_id", "materia_id"),
        ForeignKeyConstraint(
            ["año_cursado", "carrera_id", "lead_id"],
            ["cursados.año_cursado", "cursados.carrera_id", "cursados.lead_id"],
        ),
    )

    def __repr__(self) -> str:
        return f"<DBInscripcionMateria(lead_id={self.lead_id}, año_cursado={self.año_cursado}, carrera_id={self.carrera_id}, materia_id={self.materia_id}, veces_cursada={self.veces_cursada})>"
