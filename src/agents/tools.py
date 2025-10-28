import math
import re

import numexpr
from langchain_chroma import Chroma
from langchain_core.tools import BaseTool, tool
from langchain_openai import OpenAIEmbeddings
from langchain_community.utilities import SearchApiAPIWrapper
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_google_community import GoogleSearchAPIWrapper


@tool
def Google_Search(query: str) -> str:
    """A wrapper around Google Search. Use this for complex queries."""
    # The wrapper automatically finds the keys from your environment
    search_wrapper = GoogleSearchAPIWrapper()
    return search_wrapper.run(f"retrive linkedin profiles links {query}")

@tool
def SearchAPI(query: str) -> str:
    """A tool that uses the SearchApi.io service to get Google search results. 
    Useful for executing complex search queries with operators like 'site:' and boolean logic."""
    # The wrapper automatically finds the SEARCHAPI_API_KEY from your environment
    search_wrapper = SearchApiAPIWrapper()
    return search_wrapper.run(f"retrive linkedin profiles links {query}")

@tool
def DuckDuckGo_Search(query: str) -> str:
    """A wrapper around DuckDuckGo Search. Useful for when you need to answer questions about current events. 
    Input should be a search query."""
    search_run = DuckDuckGoSearchRun()
    return search_run.run(f"retrive linkedin profiles links {query}")


def calculator_func(expression: str) -> str:
    """Calculates a math expression using numexpr.

    Useful for when you need to answer questions about math using numexpr.
    This tool is only for math questions and nothing else. Only input
    math expressions.

    Args:
        expression (str): A valid numexpr formatted math expression.

    Returns:
        str: The result of the math expression.
    """

    try:
        local_dict = {"pi": math.pi, "e": math.e}
        output = str(
            numexpr.evaluate(
                expression.strip(),
                global_dict={},  # restrict access to globals
                local_dict=local_dict,  # add common mathematical functions
            )
        )
        return re.sub(r"^\[|\]$", "", output)
    except Exception as e:
        raise ValueError(
            f'calculator("{expression}") raised error: {e}.'
            " Please try again with a valid numerical expression"
        )


calculator: BaseTool = tool(calculator_func)
calculator.name = "Calculator"


# Format retrieved documents
def format_contexts(docs):
    return "\n\n".join(doc.page_content for doc in docs)


def load_chroma_db():
    # Create the embedding function for our project description database
    try:
        embeddings = OpenAIEmbeddings()
    except Exception as e:
        raise RuntimeError(
            "Failed to initialize OpenAIEmbeddings. Ensure the OpenAI API key is set."
        ) from e

    # Load the stored vector database
    chroma_db = Chroma(persist_directory="./chroma_db", embedding_function=embeddings)
    retriever = chroma_db.as_retriever(search_kwargs={"k": 5})
    return retriever


def database_search_func(query: str) -> str:
    """Searches chroma_db for information in the company's handbook."""
    # Get the chroma retriever
    retriever = load_chroma_db()

    # Search the database for relevant documents
    documents = retriever.invoke(query)

    # Format the documents into a string
    context_str = format_contexts(documents)

    return context_str


database_search: BaseTool = tool(database_search_func)
database_search.name = "Database_Search"  # Update name with the purpose of your database
