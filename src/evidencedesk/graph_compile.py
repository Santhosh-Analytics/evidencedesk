from datetime import date

from langgraph.graph import END, START, StateGraph

from evidencedesk.nodes import query_expansion
from evidencedesk.schemas.research import ResearchRequest, ResearchState

request = ResearchRequest(
    research_question=[
        "BPO to AI transistions in 2026",
        "Finance to AI/ML insdustry transistions",
    ],
    source_work_backgrounds=["BPO", "Finance"],
    countries=["India"],
    minimum_prior_experience_years=7,
    target_roles=[
        "AI/ML engineer",
        "Applied NLP Engineer",
        "Machine Learning Engineer",
    ],
    as_of_date=date.today(),
    market_lookback_months=6,
)


builder = StateGraph(ResearchState)

builder.add_node("expand_queries", query_expansion)

builder.add_edge(START, "expand_queries")
builder.add_edge("expand_queries", END)

agent = builder.compile()

# Show the agent

png_data = agent.get_graph(xray=True).draw_mermaid_png()

with open("agent_graph.png", "wb") as f:
    f.write(png_data)

initial_state = ResearchState(request=request, max_calls=5)
result = agent.invoke(initial_state)
print(result)
