import json
from langchain_aws import ChatBedrockConverse
from pydantic import ValidationError
from src.prompt.extraction import create_multi_prompt_chain, create_field_extraction_prompt
from src.db import context_loader
from src.db import insert_results
from src.models.result import DocumentClassification


def init_model():
    return ChatBedrockConverse(
        model="eu.anthropic.claude-sonnet-4-20250514-v1:0",
        region_name="eu-south-2",
        temperature=0.2,
        max_tokens=1024
    )


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
        prompt_infos = context_loader()

        # 2. Crear default prompt
        default_prompt = create_field_extraction_prompt("Documento con campos no especificados")

        # 3. Crear multi-prompt chain
        llm = init_model()
        chain = create_multi_prompt_chain(llm, prompt_infos, default_prompt)

        # 4. Ejecutar clasificación
        resultado = chain.run(nombre, contenido)

        # 5. Insertar resultado en base de datos
        insert_results(resultado)

        # 6. Responder
        return {
            "statusCode": 200,
            "body": json.dumps({
                "nombre": nombre,
                "tipo_documento": resultado.documento.tipo_documento,
                "confianza": resultado.confianza_total,
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
