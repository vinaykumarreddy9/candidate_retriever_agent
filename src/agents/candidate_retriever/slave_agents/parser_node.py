from agents.candidate_retriever.graph.state import RecruitmentState
from agents.candidate_retriever.graph.node_schema import CandidateList
from agents.candidate_retriever.graph.prompts import PARSE_AND_FORMAT_PROMPT
from langchain_core.messages import AIMessage
from core import get_model, settings

from langchain_core.runnables import RunnableConfig


async def parse_and_format_node(state: RecruitmentState, config: RunnableConfig) -> dict:
    """It parses the output from the tools in to human undrtandable format."""

    print("---NODE: Parsing and Formatting Results---")
    model = get_model(config["configurable"].get("model", settings.DEFAULT_MODEL))
    structured_llm = model.with_structured_output(CandidateList)
    prompt = PARSE_AND_FORMAT_PROMPT.format(raw_results=state["search_results"])
    response: CandidateList = await structured_llm.ainvoke(prompt)
    parsed_list = [profile.model_dump() for profile in response.candidates]

    if not parsed_list:
        final_message_content = "I was unable to find any suitable candidates based on the search results."
    else:
        markdown_lines = ["I found the following potential candidates for you:\n"]
        for i, candidate in enumerate(parsed_list, 1):
            markdown_lines.append(f"**{i}. {candidate['name']}**")
            markdown_lines.append(f"   - **Headline:** {candidate['headline']}")
            markdown_lines.append(f"   - **Snippet:** {candidate['snippet']}\n")
        final_message_content = "\n".join(markdown_lines)

    final_message = AIMessage(content=final_message_content)
    return {"parsed_candidates": parsed_list, "messages": [final_message]}