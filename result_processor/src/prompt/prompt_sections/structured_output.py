# prompt/prompt_sections/structured_output.py

def get_structured_output_format() -> str:
    return """
Retorna el resultado en el siguiente formato JSON:

{
  "expediente": {
    "id": null,
    "tipo_expediente": "<tipo_expediente>"
  },
  "documento": {
    "tipo_documento": "<tipo_documento>",
    "nombre_archivo": "<nombre_archivo>"
  },
  "campos_extraidos": [
    {
      "nombre_campo": "<campo>",
      "valor": "<valor extraído>",
      "confianza": 0.95
    }
  ],
  "confianza_total": 0.93,
  "razon": "Clasificación basada en coincidencia de encabezado y estructura"
}
""".strip()
