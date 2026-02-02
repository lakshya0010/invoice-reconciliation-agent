from langgraph.graph import StateGraph
from schemas.state import ReconciliationState
from agents.document_agent import document_agent
from agents.matching_agent import matching_agent
from agents.discrepancy_agent import discrepency_agent
from agents.resolution_agent import resolution_agent

graph = StateGraph(ReconciliationState)

graph.add_node("document", document_agent)
graph.add_node("matching", matching_agent)
graph.add_node("discrepancy", discrepency_agent)
graph.add_node("resolution", resolution_agent)

graph.set_entry_point("document")

graph.add_edge("document", "matching")
graph.add_edge("matching", "discrepancy")
graph.add_edge("discrepancy", "resolution")

app = graph.compile()