# models.py

from pydantic import BaseModel, Field
from typing import Optional, List


class ExpedienteModel(BaseModel):
    id: Optional[int]
    tipo_expediente: str


class DocumentoModel(BaseModel):
    tipo_documento: str
    nombre_archivo: str


class CampoExtraidoModel(BaseModel):
    nombre_campo: str
    valor: str
    confianza: Optional[float]


class DocumentClassification(BaseModel):
    expediente: ExpedienteModel
    documento: DocumentoModel
    campos_extraidos: List[CampoExtraidoModel] = []
    confianza_total: Optional[float]
    razon: Optional[str]
