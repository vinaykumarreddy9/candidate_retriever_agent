from langchain_core.prompts import PromptTemplate

SKILL_RETRIEVER_PROMPT = PromptTemplate.from_template(
    """You are an expert Skill-Retrieval Agent. 
    Your sole function is to analyze the provided job description and extract the two most critical technical competencies. 
    Your response MUST be a single, valid JSON object with two keys: "primary_skill" and "secondary_skill".
    Do not include any other text or formatting.
    Job Description: {job_description}
    """
)

BOOLEAN_QUERY_PROMPT = PromptTemplate.from_template(
    """You are an expert Boolean Query Engineer. 
    Your sole function is to convert the given JSON of skills into a single, precise, Google-compatible boolean search string for LinkedIn.
    **CRITICAL:** 
    Your response MUST be only the final boolean query string. 
    Do not include explanations, markdown, or extra parentheses around the quoted skills.
    The query MUST begin with `site:linkedin.com/in `. Enclose each skill in quotes and connect with AND.
    Example: site:linkedin.com/in "Skill One" AND "Skill Two"
    Skills JSON: {skills}"""
)

DATA_EXTRACTOR_PROMPT = PromptTemplate.from_template(
    """You are a specialized Data Extraction Agent. 
    Your only purpose is to use the available search tools to execute the exact query provided and return the raw results.
    - You have three tools available: `DuckDuckGo_Search`, `Google_Search`, and `SearchAPI`.
    - Choose the best tool to execute the query.
    - You must invoke a tool.
    Query to execute: {query}"""
)

PARSE_AND_FORMAT_PROMPT = PromptTemplate.from_template(
    """You are an expert data parsing agent. Your sole function is to analyze the raw text from a web search and extract candidate profiles.
    - Parse the provided raw text to identify individual candidates.
    - For each candidate, extract their full name, headline/title, and a short snippet mentioning key skills.
    - If no candidates are found, return an empty list.
    - Your output MUST be a valid JSON object conforming to the required schema.
    Raw Search Results Text: {raw_results}"""
)

SUPERVISOR_PROMPT = PromptTemplate.from_template(
    """You are a supervisor agent controlling a recruitment workflow. Based on the current state, determine the next agent to call.
    **Workflow Logic:**
    1. If `job_description` is present but `extracted_skills` is empty, choose **SkillExtractor**.
    2. If `extracted_skills` are present but `boolean_query` is empty, choose **QueryGenerator**.
    3. If `boolean_query` is present but `search_results` is empty, choose **DataExtractor**.
    4. If `search_results` is present but `parsed_candidates` is empty or not yet processed, choose **ParseAndFormat**.
    5. If `parsed_candidates` has been populated (even if it's an empty list), the workflow is complete. Choose **FINISH**.
    **Current State:**
    ```json
    {state_json}
    ```
    Decide the next agent. Your response MUST be a valid JSON object."""
)

