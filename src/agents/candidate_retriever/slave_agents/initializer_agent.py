from agents.candidate_retriever.graph.state import RecruitmentState
from langchain_core.messages import HumanMessage


def initial_state_setup(state: RecruitmentState) -> dict:
    """
    Checks for a new user request and RESETS the workflow state if found.
    This is the critical node that makes the agent reusable for multiple queries
    within the same conversation thread.
    """

    if state.get("messages") and isinstance(state["messages"][-1], HumanMessage):
        new_jd = state["messages"][-1].content
        return {
            "job_description": new_jd,
            "extracted_skills": {},
            "boolean_query": "",
            "search_results": "",
            "parsed_candidates": None,
        }
    return {}