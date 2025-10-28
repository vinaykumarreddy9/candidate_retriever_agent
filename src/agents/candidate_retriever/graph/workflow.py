from langgraph.graph import END, StateGraph
from agents.candidate_retriever.supervisor_agent import *
from agents.candidate_retriever.slave_agents.data_extractor import data_extractor_node
from agents.candidate_retriever.slave_agents.initializer_agent import initial_state_setup
from agents.candidate_retriever.slave_agents.query_generator import query_generator_node
from agents.candidate_retriever.slave_agents.skill_retriver import skill_extractor_node
from agents.candidate_retriever.slave_agents.parser_node import parse_and_format_node

builder = StateGraph(RecruitmentState)

builder.add_node("InitialSetup", initial_state_setup)
builder.add_node("Supervisor", supervisor_node)
builder.add_node("SkillExtractor", skill_extractor_node)
builder.add_node("QueryGenerator", query_generator_node)
builder.add_node("DataExtractor", data_extractor_node)
builder.add_node("ParseAndFormat", parse_and_format_node)

builder.set_entry_point("InitialSetup")
builder.add_edge("InitialSetup", "Supervisor")

builder.add_conditional_edges(
    "Supervisor",
    lambda state: state["next_agent"],
    {
        "SkillExtractor": "SkillExtractor",
        "QueryGenerator": "QueryGenerator",
        "DataExtractor": "DataExtractor",
        "ParseAndFormat": "ParseAndFormat",
        "FINISH": END,
    },
)

builder.add_edge("SkillExtractor", "Supervisor")
builder.add_edge("QueryGenerator", "Supervisor")
builder.add_edge("DataExtractor", "Supervisor")
builder.add_edge("ParseAndFormat", "Supervisor")

candidate_retrieval_agent = builder.compile()