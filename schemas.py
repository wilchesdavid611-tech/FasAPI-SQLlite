from pydantic import BaseModel, Field

class AsignaturaCrear(BaseModel):
    nombre: str
    creditos: int = Field(ge=1, le=10)
    horas_presenciales: int

class AsignaturaRespuesta(BaseModel):
    id: int
    nombre: str
    creditos: int
    horas_presenciales: int
    horas_autonomas: int
    nivel_dificultad: str

    class Config:
        from_attributes = True


class AsignaturaResumen(AsignaturaRespuesta):
    total_horas_semanales: float