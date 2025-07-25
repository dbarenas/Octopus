# models/context.py

from pydantic import BaseModel
from typing import Optional, List


class CampoContexto(BaseModel):
    nombre: str
    tipo: str
    requerido: Optional[bool] = False


class DocumentoContexto(BaseModel):
    nombre: str
    descripcion: str
    campos: List[CampoContexto] = []
