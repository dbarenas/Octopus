# prompt/extraction.py

from langchain.prompts import PromptTemplate
from prompt.prompt_sections.extraction_content import get_extraction_instructions
from prompt.prompt_sections.structured_output import get_structured_output_format


def create_field_extraction_prompt(expected_fields: list[str]) -> PromptTemplate:
    field_list = "\n".join([f"- {f}" for f in expected_fields])
    instructions = get_extraction_instructions(field_list)
    output_format = get_structured_output_format()

    template = f"""
                {instructions}

                ## CONTENIDO DEL DOCUMENTO:
                {{{{document_content}}}}

                {output_format}
                """

    return PromptTemplate(
        input_variables=["document_content"],
        template=template.strip()
    )

