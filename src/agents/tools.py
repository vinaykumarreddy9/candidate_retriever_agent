import os
from serpapi import GoogleSearch
from langchain_core.tools import tool
from typing import Any

@tool
async def SerpAPI_LinkedIn_Search(query: str, num_pages: Any = 1) -> str: # Changed to async def
    """
    Fetches Google search results for LinkedIn profile URLs using the SerpApi.
    Use this tool for targeted sourcing of LinkedIn profiles.
    The query should be a boolean search string. It fetches one page of up to 100 results.
    """
    api_key = os.getenv("SERPAPI_API_KEY")
    if not api_key:
        raise ValueError("SerpApi API key not found. Please set the 'SERPAPI_API_KEY' environment variable.")

    all_links = []
    try:
        for page_num in range(num_pages):
            start_index = page_num * 10
            params = {
                "api_key": api_key,
                "engine": "google",
                "q": query,
                "start": start_index,
                "num": 100,
            }
            search = GoogleSearch(params)
            search_results = search.get_dict()

            organic_results = search_results.get("organic_results", [])
            if not organic_results:
                break 

            for result in organic_results:
                link = result.get("link")
                if link and "linkedin.com/in/" in link:
                    all_links.append(link)
    
    except Exception as e:
        return f"SerpApi search failed with an error: {e}"

    if not all_links:
        return "No LinkedIn profiles found for the given query."
        
    unique_links = list(set(all_links))
    return "\n".join(unique_links)