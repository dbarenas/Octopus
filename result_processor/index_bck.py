import os
import json
from langchain.prompts import PromptTemplate
from langchain_aws import ChatBedrockConverse
from pydantic import BaseModel, Field
from prompts import create_document_classification_prompt

# Rehabilitacion 
documents_dict = {
    "DNI/NIE": "Documento de identidad de una persona, puede ser un DNI o NIE en caso de persona extranjera",
    
    "Proyecto de Obra Ejecutada": "Documento técnico que describe detalladamente las obras de rehabilitación ya realizadas en el edificio, incluyendo planos, memorias técnicas, presupuestos y certificaciones de los trabajos completados.",
    
    "Certificado Fin de Obra": "Documento oficial emitido por el técnico director que certifica que las obras han sido completadas conforme al proyecto y cumplen con la normativa técnica aplicable.",
    
    "Certificado Instalación Térmica": "Certificado que acredita que la instalación térmica (calefacción, refrigeración, ACS) cumple con el Reglamento de Instalaciones Térmicas en Edificios (RITE) y ha sido correctamente ejecutada.",
    
    "Certificado Eficiencia Energética": "Documento que califica energéticamente el edificio tras la rehabilitación, indicando su consumo de energía y emisiones de CO2, siendo obligatorio para demostrar la mejora energética conseguida.",
    
    "Memoria de Actuación": "Documento descriptivo que detalla las actuaciones de rehabilitación realizadas, justificando técnicamente los trabajos ejecutados y su adecuación a los objetivos de la subvención.",
    
    "Documentación Fotográfica": "Conjunto de fotografías que documentan el estado del edificio antes, durante y después de las obras, sirviendo como evidencia visual de las actuaciones realizadas.",
    
    "Declaración Otras Subvenciones": "Declaración jurada donde el solicitante informa sobre otras ayudas públicas recibidas o solicitadas para la misma actuación, evitando duplicidades y cumpliendo con la normativa de ayudas públicas.",
    
    "Pedidos y Contratos": "Documentos contractuales que formalizan los encargos de obras, servicios o suministros, estableciendo condiciones, plazos y precios para la ejecución de la rehabilitación.",
    
    "Facturas Justificantes": "Facturas y comprobantes de pago que acreditan los gastos realizados en la rehabilitación, siendo imprescindibles para justificar el uso de los fondos de la subvención.",
    
    "Título Urbanístico": "Documento que acredita la legalidad urbanística de las obras realizadas, como licencia de obras, declaración responsable o comunicación previa, según la normativa municipal aplicable.",
    
    "Puesta en Servicio de Instalaciones": "Certificado que acredita que las instalaciones renovadas o nuevas (eléctricas, térmicas, fontanería) han sido puestas en funcionamiento correctamente y cumplen con las normativas de seguridad.",
    
    "Documento No Clasificado": "Selección en caso de que el documento no pueda ser clasificado en ninguno de los documentos descritos anteriormente."
}

# Modelo Pydantic para structured output
class DocumentClassification(BaseModel):
    tipo_documento: str = Field(description="Tipo de documento clasificado")
    confianza: float = Field(description="Nivel de confianza de 0.0 a 1.0")
    razon: str = Field(description="Explicación breve de por qué se eligió este tipo")

# Configurar modelo AWS Bedrock Anthropic
def init_model():
    return ChatBedrockConverse(
        model="eu.anthropic.claude-sonnet-4-20250514-v1:0",
        region_name="eu-south-2",
        temperature=0.2,
        max_tokens=1024    
    ).with_structured_output(DocumentClassification)

# Función para clasificar un documento
def clasificar_documento(nombre_documento, contenido_documento):
    prompt = create_document_classification_prompt(documents=documents_dict)
    model = init_model()
    
    # Crear la cadena
    chain = prompt | model
    
    try:
        resultado = chain.invoke({
            "document_name": nombre_documento,
            "document_content": contenido_documento
        })
        
        return {
            'tipo_documento': resultado.tipo_documento,
            'confianza': resultado.confianza,
            'razon': resultado.razon
        }
        
    except Exception as e:
        return {
            'tipo_documento': 'Documento No Clasificado',
            'confianza': 0.0,
            'razon': f'Error en procesamiento: {str(e)}'
        }

# Lambda handler principal
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
        clasificacion = clasificar_documento(nombre, contenido)
        return {
            "statusCode": 200,
            "body": json.dumps({
                "nombre": nombre,
                "tipo_documento": clasificacion['tipo_documento'],
                "confianza": clasificacion['confianza'],
                "razon": clasificacion['razon']
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