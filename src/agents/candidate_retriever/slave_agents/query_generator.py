from agents.candidate_retriever.graph.state import RecruitmentState
from agents.candidate_retriever.graph.prompts import BOOLEAN_QUERY_PROMPT
from core import get_model, settings

import json
from langchain_core.runnables import RunnableConfig


async def query_generator_node(state: RecruitmentState, config: RunnableConfig) -> dict:
    """Query Generation Node that generates Boolean Query based on retrieved skills."""

    model = get_model(config["configurable"].get("model", settings.DEFAULT_MODEL))
    skills_str = json.dumps(state["extracted_skills"])
    prompt = BOOLEAN_QUERY_PROMPT.format(skills=skills_str)
    response = await model.ainvoke(prompt)
    return {"boolean_query": response.content.strip()}
