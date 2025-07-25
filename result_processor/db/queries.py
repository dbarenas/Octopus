# helpers.py

from models import ExpedienteModel, DocumentoModel, CampoExtraidoModel
from typing import List

# db/queries.py

GET_CONTEXT_QUERY = """
SELECT 
    td.id AS documento_id,
    td.nombre AS documento_nombre,
    td.descripcion AS documento_descripcion,
    tc.nombre AS campo_nombre,
    tc.tipo_dato AS campo_tipo,
    tc.regex_validacion,
    tdc.requerido
FROM tipo_documento td
LEFT JOIN tipo_documento_campo tdc ON td.id = tdc.tipo_documento_id
LEFT JOIN tipo_campo tc ON tdc.tipo_campo_id = tc.id
ORDER BY td.id, tdc.posicion;
"""


def get_or_create_tipo_expediente(cur, tipo_expediente_nombre: str) -> int:
    cur.execute("SELECT id FROM tipo_expediente WHERE nombre = %s", (tipo_expediente_nombre,))
    row = cur.fetchone()
    if row:
        return row[0]
    cur.execute(
        "INSERT INTO tipo_expediente (nombre) VALUES (%s) RETURNING id",
        (tipo_expediente_nombre,)
    )
    return cur.fetchone()[0]


def get_or_create_expediente(cur, expediente: ExpedienteModel, tipo_expediente_id: int) -> int:
    if expediente.id is not None:
        return expediente.id
    cur.execute(
        "INSERT INTO expediente (tipo_expediente_id) VALUES (%s) RETURNING id",
        (tipo_expediente_id,)
    )
    return cur.fetchone()[0]


def get_tipo_documento_id(cur, tipo_documento_nombre: str) -> int:
    cur.execute("SELECT id FROM tipo_documento WHERE nombre = %s", (tipo_documento_nombre,))
    row = cur.fetchone()
    if not row:
        raise ValueError(f"Tipo documento '{tipo_documento_nombre}' no encontrado en base de datos")
    return row[0]


def insert_documento(cur, documento: DocumentoModel, expediente_id: int, tipo_documento_id: int) -> int:
    cur.execute(
        """
        INSERT INTO documento (tipo_documento_id, expediente_id, nombre_archivo)
        VALUES (%s, %s, %s) RETURNING id
        """,
        (tipo_documento_id, expediente_id, documento.nombre_archivo)
    )
    return cur.fetchone()[0]


def insert_campos_extraidos(cur, campos: List[CampoExtraidoModel], documento_id: int, tipo_documento_id: int):
    for campo in campos:
        cur.execute(
            """
            SELECT tc.id
            FROM tipo_campo tc
            JOIN tipo_documento_campo tdc ON tc.id = tdc.tipo_campo_id
            WHERE tdc.tipo_documento_id = %s AND tc.nombre = %s
            """,
            (tipo_documento_id, campo.nombre_campo)
        )
        row = cur.fetchone()
        if not row:
            continue
        tipo_campo_id = row[0]
        cur.execute(
            """
            INSERT INTO campo_extraido (documento_id, tipo_campo_id, valor, confianza, estado_validacion)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (documento_id, tipo_campo_id, campo.valor, campo.confianza, "pendiente")
        )
