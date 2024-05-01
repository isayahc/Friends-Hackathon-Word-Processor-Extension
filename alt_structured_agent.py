from langchain.agents import AgentExecutor
from langchain.retrievers import PubMedRetriever
from langchain.agents.format_scratchpad import format_to_openai_function_messages
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI
import json

from langchain_core.agents import AgentActionMessageLog, AgentFinish
from typing import List

from langchain_core.pydantic_v1 import BaseModel, Field

class Response(BaseModel):
    """Final response to the question being asked"""

    answer: str = Field(description="The final answer to respond to the user")
    genes: List[str] = Field(
        description="The list of genes one or many genes that can be used to solve the problem statement provide by the user"
    )

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a helpful assistant"),
        ("user", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ]
)

def parse(output):
    # If no function was invoked, return to user
    if "function_call" not in output.additional_kwargs:
        return AgentFinish(return_values={"output": output.content}, log=output.content)

    # Parse out the function call
    function_call = output.additional_kwargs["function_call"]
    name = function_call["name"]
    inputs = json.loads(function_call["arguments"])

    # If the Response function was invoked, return to the user with the function inputs
    if name == "Response":
        return AgentFinish(return_values=inputs, log=str(function_call))
    # Otherwise, return an agent action
    else:
        return AgentActionMessageLog(
            tool=name, tool_input=inputs, log="", message_log=[output]
        )

llm = ChatOpenAI(temperature=0)

from langchain.tools.retriever import create_retriever_tool

# @tool
# def wikipedia_search(query: str) -> str:
#      """Search Wikipedia for additional information to expand on research papers or when no papers can be found."""
#     global all_sources

#     api_wrapper = WikipediaAPIWrapper()
#     wikipedia_search = WikipediaQueryRun(api_wrapper=api_wrapper)
#     wikipedia_results = wikipedia_search.run(query)
#     formatted_summaries = format_wiki_summaries(wikipedia_results)
#     all_sources += formatted_summaries
#     parsed_summaries = parse_list_to_dicts(formatted_summaries)
#     # add_many(parsed_summaries)
#     #all_sources += create_wikipedia_urls_from_text(wikipedia_results)
#     return wikipedia_results

retriever_tool = create_retriever_tool(
    PubMedRetriever(),
    "biotech-research",
    "Query a retriever to get information about the genes that could solve the requested solution",
)

llm_with_tools = llm.bind_functions([retriever_tool, Response])

agent = (
    {
        "input": lambda x: x["input"],
        # Format agent scratchpad from intermediate steps
        "agent_scratchpad": lambda x: format_to_openai_function_messages(
            x["intermediate_steps"]
        ),
    }
    | prompt
    | llm_with_tools
    | parse
)

agent_executor = AgentExecutor(tools=[retriever_tool], agent=agent, verbose=True)

sample = agent_executor.invoke(
    {"input": "I am looking for a gene that can be used to prevent drought"},
    return_only_outputs=True,
)
x = 0
