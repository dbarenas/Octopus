# Imagen base oficial de AWS Lambda para Python 3.11
FROM public.ecr.aws/lambda/python:3.11

# Establecer variables de entorno para versiones
ENV PILLOW_VERSION=11.3.0 \
    TEXTRACTOR_VERSION=1.9.2 \
    PANDAS_VERSION=2.3.1 \
    NUMPY_VERSION=1.26.4 \
    LANGGRAPH_VERSION=0.5.3 \
    LANGCHAIN_VERSION=0.3.26 \
    LANGCHAIN_AWS_VERSION=0.2.28 \
    LANGCHAIN_COMMUNITY=0.3.26

# Instalar dependencias y librerías
RUN pip install --upgrade pip \
 && pip install \
    Pillow==${PILLOW_VERSION} \
    amazon-textract-textractor==${TEXTRACTOR_VERSION} \
    pandas==${PANDAS_VERSION} \
    numpy==${NUMPY_VERSION} \
    langchain==${LANGCHAIN_VERSION} \
    langchain-aws==${LANGCHAIN_AWS_VERSION} \
    langchain-community==${LANGCHAIN_COMMUNITY} \
    langgraph==${LANGGRAPH_VERSION}
    

# Copiar tu código a la imagen
COPY index.py ${LAMBDA_TASK_ROOT}
COPY prompts.py ${LAMBDA_TASK_ROOT}

# Definir el handler

CMD ["index.lambda_handler"]