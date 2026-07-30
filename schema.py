from pydantic import BaseModel

class ModuloCrear(BaseModel):
    titulo: str
    lenguaje: str
    horas: int
    disponible: bool = True

class ModuloRespuesta(ModuloCrear):
    id: int

    class Config:
        from_attributes = True