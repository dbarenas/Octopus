from langchain.prompts import PromptTemplate
from typing import Dict

def create_document_classification_prompt(documents: Dict[str, str]) -> PromptTemplate:
    """
    Crea el prompt de clasificación basado en los tipos de documentos disponibles
    
    Args:
        documents: Dict con formato {tipo_documento: descripción}
        
    Returns:
        PromptTemplate configurado para clasificación
    """
    
    # Construir la sección de tipos de documentos disponibles
    document_types_section = ""
    for doc_type, doc_description in documents.items():
        document_types_section += f"- **{doc_type}**: {doc_description}\n"
    
    prompt_template = f"""
Eres un experto en clasificación de documentos. Tu tarea es analizar el contenido de un documento y clasificarlo en uno de los tipos disponibles.

## TIPOS DE DOCUMENTOS DISPONIBLES:
{document_types_section}

## INSTRUCCIONES:
1. Lee cuidadosamente el contenido del documento
2. Analiza las características clave, estructura y contenido
3. Considera también el nombre del archivo como pista adicional
4. Compara con las descripciones de los tipos disponibles
5. Selecciona el tipo más apropiado
6. Asigna un nivel de confianza del 0.0 al 1.0

## NOMBRE DEL DOCUMENTO:
{{document_name}}

## CONTENIDO DEL DOCUMENTO:
```
{{document_content}}
```

Clasifica el documento usando el formato de salida estructurado requerido."""

    return PromptTemplate(
        input_variables=["document_name", "document_content"],
        template=prompt_template
    )