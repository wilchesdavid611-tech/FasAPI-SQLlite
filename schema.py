from pydantic import BaseModel

class AprendizCREAR(BaseModel):
    nombre: str
    documento: str
    programa : str

class AprendizRespuesta(AprendizCREAR):
    id: int

class config:
    from_atribute = True