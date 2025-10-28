from agents.candidate_retriever.graph.state import RecruitmentState
from langchain_core.messages import HumanMessage


def initial_state_setup(state: RecruitmentState) -> dict:
    """
    Checks for a new user request and RESETS the workflow state if found.
    This is the critical node that makes the agent reusable for multiple queries
    within the same conversation thread.
    """
    # Check if the last message is from the user.
    if state.get("messages") and isinstance(state["messages"][-1], HumanMessage):
        print("---NODE: New user request detected. Resetting workflow state.---")
        new_jd = state["messages"][-1].content
        # This dictionary explicitly clears all previous workflow products.
        return {
            "job_description": new_jd,
            "extracted_skills": {},
            "boolean_query": "",
            "search_results": "",
            "parsed_candidates": None, # Reset to a non-list value
        }
    return {}