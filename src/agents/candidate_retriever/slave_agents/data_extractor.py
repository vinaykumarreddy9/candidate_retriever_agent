from agents.candidate_retriever.graph.state import RecruitmentState
from agents.candidate_retriever.graph.prompts import DATA_EXTRACTOR_PROMPT
from agents.tools import DuckDuckGo_Search, Google_Search,SearchAPI
from langchain_core.messages import ToolMessage
from core import get_model, settings

from langchain_core.runnables import RunnableConfig


async def data_extractor_node(state: RecruitmentState, config: RunnableConfig) -> dict:
    """Data extraction agent that extracts data besed on Boolean query from the web."""

    print("---NODE: Extracting Data from Web---")
    model = get_model(config["configurable"].get("model", settings.DEFAULT_MODEL))
    tools = [DuckDuckGo_Search, Google_Search, SearchAPI]
    
    # We use a simple agent that is forced to call a tool
    prompt = DATA_EXTRACTOR_PROMPT.format(query=state['boolean_query'])
    agent_runnable = model.bind_tools(tools)
    response = await agent_runnable.ainvoke(prompt)
    
    # response is an AIMessage with tool_calls
    tool_message = ToolMessage(content="No tool was called by the agent.", tool_call_id="")
    if response.tool_calls:
        tool_call = response.tool_calls[0]
        tool_to_use = {"Google_Search": Google_Search, "DuckDuckGo_Search": DuckDuckGo_Search, "SearchAPI": SearchAPI}[tool_call['name']]
        tool_output = await tool_to_use.ainvoke(tool_call['args'])
        tool_message = ToolMessage(content=str(tool_output), tool_call_id=tool_call['id'])

    return {"search_results": tool_message.content}

