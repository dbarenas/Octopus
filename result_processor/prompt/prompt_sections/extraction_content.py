# prompt/prompt_sections/extraction_content.py

def get_extraction_instructions(expected_fields_section: str) -> str:
    return f"""
Eres un sistema experto en extracción de datos. Tu tarea es extraer los siguientes campos del contenido del documento.

## CAMPOS ESPERADOS:
{expected_fields_section}

## INSTRUCCIONES:
1. Analiza el contenido y estructura del documento.
2. Extrae el valor de cada campo si está presente.
3. Para cada campo, indica un valor de confianza entre 0.0 y 1.0.
4. Si un campo no está presente, déjalo vacío o no lo incluyas.
""".strip()
