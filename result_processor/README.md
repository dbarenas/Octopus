# Procesador de Resultados

Este proyecto contiene una función Lambda para la clasificación de documentos.

## Estructura del Proyecto

- `src/`: Contiene el código fuente de la función Lambda.
  - `db/`: Contiene módulos para interactuar con la base de datos.
    - `connector.py`: Gestiona la conexión con la base de datos.
    - `context_loader.py`: Carga el contexto del documento desde la base de datos.
    - `insert_results.py`: Inserta los resultados de la clasificación en la base de datos.
    - `queries.py`: Contiene las consultas SQL.
  - `models/`: Contiene los modelos Pydantic para la validación de datos.
    - `context.py`: Define los modelos de contexto.
    - `result.py`: Define los modelos de resultado.
  - `prompt/`: Contiene módulos para crear los prompts de clasificación.
    - `classification.py`: Crea el prompt de clasificación de documentos.
    - `prompt_sections/`: Contiene las diferentes secciones del prompt.
- `index.py`: El punto de entrada principal de la función Lambda.
- `requirements.txt`: Las dependencias del proyecto.

## Cómo Ejecutar

1. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```
2. Crea un archivo zip para la función Lambda:
   ```bash
   cd result_processor
   zip -r ../result_processor.zip .
   ```
3. Sube el archivo `result_processor.zip` a tu función Lambda.
