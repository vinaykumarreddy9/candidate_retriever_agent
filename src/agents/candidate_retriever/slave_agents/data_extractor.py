from agents.candidate_retriever.graph.state import RecruitmentState
from agents.candidate_retriever.graph.prompts import DATA_EXTRACTOR_PROMPT
from agents.tools import SerpAPI_LinkedIn_Search
from langchain_core.messages import AIMessage
from core import get_model, settings
from langchain_core.runnables import RunnableConfig


async def data_extractor_node(state: RecruitmentState, config: RunnableConfig) -> dict:
    """
    Data extraction agent that finds profile URLs and formats the final response.
    """
    model = get_model(config["configurable"].get("model", settings.DEFAULT_MODEL))
    tools = [SerpAPI_LinkedIn_Search]
    
    prompt = DATA_EXTRACTOR_PROMPT.format(query=state['boolean_query'])
    
    agent_runnable = model.bind_tools(tools)
    response = await agent_runnable.ainvoke(prompt)
    
    search_content = "The agent failed to call the search tool."
    
    if response.tool_calls:
        tool_call = response.tool_calls[0]
        tool_output = await SerpAPI_LinkedIn_Search.ainvoke(tool_call['args'])
        search_content = str(tool_output)

    if "No LinkedIn profiles found" in search_content or "failed" in search_content:
        final_message_content = "I was unable to find any suitable candidates for your query."
    else:
        urls = search_content.strip().split('\n')
        markdown_links = "\n".join(f"- {url}" for url in urls)
        final_message_content = f"I found the following {len(urls)} LinkedIn profiles for you:\n\n{markdown_links}"

    final_message = AIMessage(content=final_message_content)

    return {
        "search_results": search_content,
        "messages": [final_message]
    }