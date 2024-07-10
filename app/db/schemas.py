from pydantic import BaseModel


class Lead(BaseModel):
    id: int
    nombre: str
    apellido: str
    direccion: str
    tel: int


class Carrera(BaseModel):
    id: int
    nombre: str


class Materia(BaseModel):
    id: int
    nombre: str
    carrera_id: int


class Cursado(BaseModel):
    año_cursado: int
    carrera_id: int
    lead_id: int
    universidad: str


class InscripcionMateria(BaseModel):
    año_cursado: int
    carrera_id: int
    lead_id: int
    materia_id: int
    veces_cursada: int
