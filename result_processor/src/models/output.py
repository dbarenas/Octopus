from pydantic import BaseModel, Field
from typing import List

class CampoExtraido(BaseModel):
    nombre_campo: str
    valor: str
    confianza: float

class OutputModel(BaseModel):
    expediente: dict
    documento: dict
    campos_extraidos: List[CampoExtraido]
    confianza_total: float
    razon: str
