from typing import TypedDict, Annotated, Literal, List
from pydantic import BaseModel, Field


class CandidateProfile(BaseModel):
    """Represents a single parsed candidate profile."""
    name: str = Field(description="The full name of the candidate.")
    headline: str = Field(description="The candidate's current title or professional headline.")
    snippet: str = Field(description="A brief, relevant snippet from their profile mentioning the key skills.")

class CandidateList(BaseModel):
    """A list of parsed candidate profiles."""
    candidates: List[CandidateProfile]

class SupervisorDecision(BaseModel):
    """The decision of the supervisor on which agent to run next."""
    next_agent: Literal["SkillExtractor", "QueryGenerator", "DataExtractor", "ParseAndFormat", "FINISH"] = Field(
        description="The next agent to route to, based on the current state."
    )