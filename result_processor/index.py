import json
from langchain_aws import ChatBedrockConverse
from pydantic import ValidationError
from prompt.classification import create_document_classification_prompt
from db import context_loader
from db import insert_results  # función que inserta el resultado en la BD
from models.result import DocumentClassification  # Pydantic model
from langchain.prompts import PromptTemplate


def init_model():
    return ChatBedrockConverse(
        model="eu.anthropic.claude-sonnet-4-20250514-v1:0",
        region_name="eu-south-2",
        temperature=0.2,
        max_tokens=1024
    ).with_structured_output(DocumentClassification)


def clasificar_documento(nombre_documento: str, contenido_documento: str, documents_dict: dict) -> DocumentClassification:
    prompt = create_document_classification_prompt(documents=documents_dict)
    model = init_model()
    chain = prompt | model

    resultado = chain.invoke({
        "document_name": nombre_documento,
        "document_content": contenido_documento
    })
    return resultado  # Instancia DocumentClassification


def lambda_handler(event, context):
    contenido = event.get("contenido")
    nombre = event.get("nombre", "Sin nombre")

    if not contenido:
        return {
            "statusCode": 400,
            "body": json.dumps({
                "nombre": nombre,
                "tipo_documento": "Error",
                "confianza": 0.0,
                "razon": "Sin contenido de documento"
            }, ensure_ascii=False)
        }

    try:
        # 1. Obtener contexto actualizado desde BD
        documentos_dict = context_loader()

        # 2. Ejecutar clasificación
        resultado = clasificar_documento(nombre, contenido, documentos_dict)

        # 3. Insertar resultado en base de datos
        # Aquí deberías construir el dict esperado para insert_results
        resultado_insert = {
            "expediente": {
                "id": None,
                "tipo_expediente": "Clasificación automática"
            },
            "documento": {
                "tipo_documento": resultado.tipo_documento,
                "nombre_archivo": nombre
            },
            "campos_extraidos": [],  # en clasificación normalmente no extraes campos
            "confianza_total": resultado.confianza,
            "razon": resultado.razon
        }
        insert_results(resultado_insert)

        # 4. Responder
        return {
            "statusCode": 200,
            "body": json.dumps({
                "nombre": nombre,
                "tipo_documento": resultado.tipo_documento,
                "confianza": resultado.confianza,
                "razon": resultado.razon
            }, ensure_ascii=False)
        }

    except ValidationError as ve:
        # Error en validación Pydantic
        return {
            "statusCode": 500,
            "body": json.dumps({
                "nombre": nombre,
                "tipo_documento": "Error",
                "confianza": 0.0,
                "razon": f"Error de validación: {ve.errors()}"
            }, ensure_ascii=False)
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({
                "nombre": nombre,
                "tipo_documento": "Error",
                "confianza": 0.0,
                "razon": f"Error en clasificación: {str(e)}"
            }, ensure_ascii=False)
        }
