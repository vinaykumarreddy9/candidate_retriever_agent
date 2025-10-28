from agents.candidate_retriever.graph.state import RecruitmentState
from agents.candidate_retriever.graph.node_schema import SupervisorDecision
from agents.candidate_retriever.graph.prompts import SUPERVISOR_PROMPT
from core import get_model, settings

import json
from langchain_core.runnables import RunnableConfig


async def supervisor_node(state: RecruitmentState, config: RunnableConfig) -> dict:
    """Supervisor agent that handles the workflow. It decides the flow of an agent."""

    print("---NODE: Supervisor Deciding Next Step---")
    model = get_model(config["configurable"].get("model", settings.DEFAULT_MODEL))
    structured_llm = model.with_structured_output(SupervisorDecision)
    state_snapshot = state.copy()
    state_snapshot.pop("messages", None)
    state_snapshot['parsed_candidates'] = state.get('parsed_candidates', 'NOT_PROCESSED') # Make state clearer for LLM
    state_json = json.dumps(state_snapshot, indent=2)
    prompt = SUPERVISOR_PROMPT.format(state_json=state_json)
    response: SupervisorDecision = await structured_llm.ainvoke(prompt)
    print(f"Supervisor chose: {response.next_agent}")
    return {"next_agent": response.next_agent}