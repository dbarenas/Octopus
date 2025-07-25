# prompt/extraction.py

from langchain.prompts import ChatPromptTemplate
from langchain.output_parsers import PydanticOutputParser
from src.models.output import OutputModel
from prompt.prompt_sections.extraction_content import get_extraction_instructions
from langchain.chains.router import MultiPromptChain
from langchain.chains.llm import LLMChain
from langchain.chains.router.multi_prompt_prompt import MULTI_PROMPT_ROUTER_TEMPLATE

def create_field_extraction_prompt(context: str = "") -> ChatPromptTemplate:
    parser = PydanticOutputParser(pydantic_object=OutputModel)
    instructions = get_extraction_instructions()

    template = f"""
                {instructions}

                Contexto: {context}

                {{format_instructions}}

                ## CONTENIDO DEL DOCUMENTO:
                {{{{document_content}}}}
                """

    return ChatPromptTemplate.from_template(
        template.strip(),
        partial_variables={"format_instructions": parser.get_format_instructions()},
    )

def create_multi_prompt_chain(llm, prompt_infos, default_prompt):
    """
    Creates a MultiPromptChain from a list of prompt infos.
    """

    chains = {}
    for prompt_info in prompt_infos:
        prompt = create_field_extraction_prompt(prompt_info["description"])
        chain = LLMChain(llm=llm, prompt=prompt)
        chains[prompt_info["name"]] = chain

    default_chain = LLMChain(llm=llm, prompt=default_prompt)

    router_chain = MultiPromptChain.from_prompts(
        llm=llm,
        prompt_infos=prompt_infos,
        default_chain=default_chain,
        chains=chains,
        router_prompt=MULTI_PROMPT_ROUTER_TEMPLATE,
        verbose=True,
    )

    return router_chain
