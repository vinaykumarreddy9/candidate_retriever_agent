from typing import TypedDict, Annotated, Literal, List

class RecruitmentState(TypedDict):
    messages: Annotated[list, lambda x, y: x + y]
    job_description: str
    extracted_skills: dict
    boolean_query: str
    search_results: str
    next_agent: Literal["SkillExtractor", "QueryGenerator", "DataExtractor", "FINISH"]
