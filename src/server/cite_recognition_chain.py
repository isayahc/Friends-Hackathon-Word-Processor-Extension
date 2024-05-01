from langchain.output_parsers import ResponseSchema, StructuredOutputParser
from langchain.prompts import PromptTemplate
from langchain_community.llms import HuggingFaceEndpoint
from langchain_core.runnables import RunnablePassthrough

from dotenv import load_dotenv

import os

from langchain_community.chat_models.anthropic import (
    ChatAnthropic
    )

load_dotenv()

response_schemas = [
    ResponseSchema(name="is_str_a_source", description="Determine with APA citation", type="bool"),
]

output_parser = StructuredOutputParser.from_response_schemas(response_schemas)

format_instructions = output_parser.get_format_instructions()

prompt = maker_prompt = PromptTemplate(
    # template="You will be given a string of text and you must determine if the string is APA citation or not. Please repond 'yes' or 'no' Only repond 'yes' or 'no'\n{question}\n",
    template="You are a researcher at a biotech laboratory with a speciality in Saccharomyces cerevisiae. You are also able to search the internet gor transgenes you can try from different organisms  \n{question}\n",
    # template="You must generate a well detailed list of items for creating a given item from scratch. \
    #     Also describe the purpose for a text-to-3d model to use for extra context\n{format_instructions}\n{question}\n{context}",
    input_variables=["question"],
    # partial_variables={"format_instructions": format_instructions},
    # memory = memory
)

def join_strings(*args: str) -> str:
    """
    Join an arbitrary number of strings into one string.
    
    Args:
        *args: Variable number of strings to join.
    
    Returns:
        str: Joined string.
    """
    return ''.join(args)

def format_docs(docs):
    return "\n\n".join([join_strings(d.page_content, d.metadata['Entry ID'],d.metadata['Title'], ) for d in docs])

# model = llm = HuggingFaceEndpoint(repo_id="mistralai/Mixtral-8x7B-Instruct-v0.1", 
#                         temperature=0.1, 
#                         max_new_tokens=3,
#                         repetition_penalty=1.2,
#                         return_full_text=False
#     )
ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY')
llm = ChatAnthropic(
    anthropic_api_key=ANTHROPIC_API_KEY,
    )

cite_chain = (
# {
#     "context": arxiv_retriever, 
#     "question": RunnablePassthrough()
#     }
prompt
| llm
# | output_parser
)

if __name__ == "__main__":
    

    query_1 = "International Tennis Federation. (n.d.). Tennis. In Wikipedia. Retrieved March 22, 2023, from https://en.wikipedia.org/wiki/Tennis"
    query_2 = "Data analysist"
    query_3 = "Hi my name is jack the bozo"
    # query_4 = "I am looking for a gene that can be used to prevent flooding in the eastern us area"
    query_4 = "I am looking for a gene that can be used to prevent drought"
    # query_2 = "This is mw walking doen the street"
    
    
    # sample_1 = cite_chain.invoke(query_1)
    # sample_2 = cite_chain.invoke(query_2)
    # sample_3 = cite_chain.invoke(query_3)
    sample_4 = cite_chain.invoke(query_4)
    x=0