from pydantic import BaseModel
from typing import Optional, List


class Lead(BaseModel):
    lead_id: int
    nombre: str
    apellido: str
    email: Optional[str] = None
    direccion: Optional[str] = None
    tel: Optional[int] = None


class Carrera(BaseModel):
    carrera_id: int
    nombre: str


class Materia(BaseModel):
    materia_id: int
    nombre: str
    carrera_id: int


class Cursado(BaseModel):
    año_cursado: int
    carrera_id: int
    lead_id: int
    universidad: Optional[str]


class InscripcionMateria(BaseModel):
    año_cursado: int
    carrera_id: int
    lead_id: int
    materia_id: int
    veces_cursada: int


class LeadCreate(BaseModel):
    nombre: str
    apellido: str
    email: Optional[str] = None
    direccion: Optional[str] = None
    tel: Optional[int] = None

    cursados: List[Cursado]


class CarreraCreate(BaseModel):
    nombre: str

    materia: List[Materia]


class MateriaCreate(BaseModel):
    nombre: str
    carrera_id: int

    carrera: Carrera


class CursadoCreate(BaseModel):
    año_cursado: int
    carrera_id: int
    lead_id: int
    universidad: Optional[str]

    carrera: Carrera
    lead: Lead
    inscripciones: List[InscripcionMateria]


class InscripcionMateriaCreate(BaseModel):
    año_cursado: int
    carrera_id: int
    lead_id: int
    materia_id: int
    veces_cursada: int

    carrera: Carrera
    lead: Lead
    materia: Materia
