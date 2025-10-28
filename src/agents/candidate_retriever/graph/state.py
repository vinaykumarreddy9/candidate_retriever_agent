from typing import TypedDict, Annotated, Literal, List

class RecruitmentState(TypedDict):
    messages: Annotated[list, lambda x, y: x + y]
    job_description: str
    extracted_skills: dict
    boolean_query: str
    search_results: str  # This will hold the RAW search results
    parsed_candidates: list  # This will hold the STRUCTURED list of candidates
    next_agent: Literal["SkillExtractor", "QueryGenerator", "DataExtractor", "ParseAndFormat", "FINISH"]
