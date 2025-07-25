# prompt/classification.py

from langchain.prompts import PromptTemplate
from db import context_loader
from prompt.prompt_sections.classification_content import get_classification_instructions
from prompt.prompt_sections.structured_output import get_structured_output_format


def create_document_classification_prompt() -> PromptTemplate:
    documents = context_loader()

    document_types_section = "\n".join([
        f"- **{name}**: {desc}" for name, desc in documents.items()
    ])

    instructions = get_classification_instructions(document_types_section)
    output_format = get_structured_output_format()

    template = f"""
            {instructions}

            ## NOMBRE DEL DOCUMENTO:
            {{{{document_name}}}}

            ## CONTENIDO DEL DOCUMENTO:

            {{{{document_content}}}}

            {output_format}
            """

    return PromptTemplate(
        input_variables=["document_name", "document_content"],
        template=template.strip()
    )
