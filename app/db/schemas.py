from pydantic import BaseModel
from typing import Optional, List


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
