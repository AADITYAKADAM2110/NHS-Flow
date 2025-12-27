from langgraph.graph import StateGraph, END
from state import NHSFlowState
from nodes import analyze_ward_state, plan_logistics, human_review


builder = StateGraph(NHSFlowState)

builder.add_node("analyze", analyze_ward_state)
builder.add_node("logistics", plan_logistics)
builder.add_node("human", human_review)

builder.set_entry_point("analyze")

builder.add_conditional_edges(
    "analyze",
    lambda state: "logistics" if state["shortage_detected"] else END
)

builder.add_edge("logistics", "human")
builder.add_edge("human", END)

graph = builder.compile()