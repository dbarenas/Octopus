# insert_results.py

from src.db.connector import get_db_connection
from src.models.result import DocumentClassification
from src.db.queries import (
    get_or_create_tipo_expediente,
    get_or_create_expediente,
    get_tipo_documento_id,
    insert_documento,
    insert_campos_extraidos
)

def insert_results(resultado: DocumentClassification):
    conn = get_db_connection()
    try:
        with conn:
            with conn.cursor() as cur:
                tipo_expediente_id = get_or_create_tipo_expediente(cur, resultado.expediente.tipo_expediente)
                expediente_id = get_or_create_expediente(cur, resultado.expediente, tipo_expediente_id)
                tipo_documento_id = get_tipo_documento_id(cur, resultado.documento.tipo_documento)
                documento_id = insert_documento(cur, resultado.documento, expediente_id, tipo_documento_id)
                insert_campos_extraidos(cur, resultado.campos_extraidos, documento_id, tipo_documento_id)

        return {
            "status": "success",
            "expediente_id": expediente_id,
            "documento_id": documento_id
        }

    except Exception as e:
        conn.rollback()
        return {
            "status": "error",
            "error": str(e)
        }
    finally:
        conn.close()
