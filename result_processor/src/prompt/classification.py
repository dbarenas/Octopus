# prompt/classification.py

from langchain.prompts import PromptTemplate
from src.db import context_loader
from src.prompt.prompt_sections.classification_content import get_classification_instructions


def create_document_classification_prompt(documents: dict) -> PromptTemplate:
    document_types_section = "\n".join([
        f"- **{name}**: {desc}" for name, desc in documents.items()
    ])

    instructions = get_classification_instructions(document_types_section)

    template = f"""
            {instructions}

            ## NOMBRE DEL DOCUMENTO:
            {{{{document_name}}}}

            ## CONTENIDO DEL DOCUMENTO:

            {{{{document_content}}}}
            """

    return PromptTemplate(
        input_variables=["document_name", "document_content"],
        template=template.strip()
    )
