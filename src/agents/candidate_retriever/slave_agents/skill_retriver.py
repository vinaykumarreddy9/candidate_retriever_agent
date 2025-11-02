from agents.candidate_retriever.graph.state import RecruitmentState
from agents.candidate_retriever.graph.prompts import SKILL_RETRIEVER_PROMPT
from core import get_model, settings

import json
from langchain_core.runnables import RunnableConfig


async def skill_extractor_node(state: RecruitmentState, config: RunnableConfig) -> dict:
    """Skill extractor node that extract the skills from job description."""

    model = get_model(config["configurable"].get("model", settings.DEFAULT_MODEL))
    prompt = SKILL_RETRIEVER_PROMPT.format(job_description=state["job_description"])
    response = await model.ainvoke(prompt)
    try:
        extracted_json = json.loads(response.content)
        return {"extracted_skills": extracted_json}
    except json.JSONDecodeError:
        return {"extracted_skills": {"error": "Failed to parse skills JSON from LLM."}}

