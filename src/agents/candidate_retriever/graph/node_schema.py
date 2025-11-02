from pydantic import BaseModel, Field
from typing import Literal


class SupervisorDecision(BaseModel):
    """The decision of the supervisor on which agent to run next."""
    next_agent: Literal["SkillExtractor", "QueryGenerator", "DataExtractor", "FINISH"] = Field(
        description="The next agent to route to, based on the current state."
    )