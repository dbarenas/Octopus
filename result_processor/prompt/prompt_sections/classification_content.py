# prompt/prompt_sections/classification_content.py

def get_classification_instructions(document_types_section: str) -> str:
    return f"""
Eres un experto en clasificación de documentos. Tu tarea es analizar el contenido y clasificarlo según los tipos disponibles.

## TIPOS DE DOCUMENTOS DISPONIBLES:
{document_types_section}

## INSTRUCCIONES:
1. Lee cuidadosamente el contenido del documento.
2. Analiza estructura, contenido y nombre del archivo.
3. Compara con las descripciones anteriores.
4. Selecciona el tipo más apropiado.
5. Asigna un nivel de confianza entre 0.0 y 1.0.
""".strip()
