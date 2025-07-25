# db/context.py

import pandas as pd
from db.connector import get_db_connection
from db.queries import GET_CONTEXT_QUERY
from models.context import DocumentoContexto, CampoContexto


def context_loader():
    conn = get_db_connection()
    df = pd.read_sql(GET_CONTEXT_QUERY, conn)
    conn.close()

    contexto: dict[str, DocumentoContexto] = {}

    for _, row in df.iterrows():
        nombre_doc = row["documento_nombre"]
        descripcion = row["documento_descripcion"]

        if nombre_doc not in contexto:
            contexto[nombre_doc] = DocumentoContexto(
                nombre=nombre_doc,
                descripcion=descripcion,
                campos=[]
            )

        if pd.notna(row["campo_nombre"]):
            campo = CampoContexto(
                nombre=row["campo_nombre"],
                tipo=row["campo_tipo"],
                requerido=row["requerido"]
            )
            contexto[nombre_doc].campos.append(campo)

    documents_dict = {}
    for doc in contexto.values():
        campos = "\n- ".join([
            f"{c.nombre} ({c.tipo}){' [requerido]' if c.requerido else ''}"
            for c in doc.campos
        ])
        descripcion_completa = (
            f"{doc.descripcion}\nCampos esperados:\n- {campos}"
            if doc.campos else doc.descripcion
        )
        documents_dict[doc.nombre] = descripcion_completa

    documents_dict["Documento No Clasificado"] = (
        "Selección en caso de que el documento no pueda ser clasificado en ninguno de los documentos descritos anteriormente."
    )

    return documents_dict
