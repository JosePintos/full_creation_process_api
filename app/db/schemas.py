from pydantic import BaseModel
from typing import Optional, List


# Custom class exception to not raise http exception in repository since that's part of the api, not db
class NotFoundException(Exception):
    def __init__(self, message: str) -> None:
        self.message = message


class MateriaCreate(BaseModel):
    nombre: str


class CarreraCreate(BaseModel):
    nombre: str


class InscripcionMateriaCreate(BaseModel):
    materia: MateriaCreate
    veces_cursada: int


class CursadoCreate(BaseModel):
    carrera: CarreraCreate
    año_cursado: int
    universidad: Optional[str]
    inscripciones: List[InscripcionMateriaCreate]


class Lead(BaseModel):
    lead_id: int
    nombre: str
    apellido: str
    email: Optional[str]
    direccion: Optional[str]
    tel: Optional[int]
    cursados: List[CursadoCreate]


class LeadCreate(BaseModel):
    nombre: str
    apellido: str
    email: Optional[str]
    direccion: Optional[str]
    tel: Optional[int]
    cursados: List[CursadoCreate]


class LeadReturn(BaseModel):
    lead_id: int
