from langgraph.graph import END, START, StateGraph

from src.agents.nodes.browser_node import browser_node
from src.agents.nodes.coder_node import coder_node
from src.agents.nodes.coordinator_node import coordinator_node
from src.agents.nodes.planner_node import planner_node
from src.agents.nodes.reporter_node import reporter_node
from src.agents.nodes.researcher_node import researcher_node
from src.agents.nodes.supervisor_node import supervisor_node
from src.graph.types import State

def build_graph():
    """Build and return the agent workflow graph."""
    builder = StateGraph(State)

    # Define nodes
    builder.add_node("coordinator", coordinator_node)
    builder.add_node("planner", planner_node)
    builder.add_node("supervisor", supervisor_node)
    builder.add_node("researcher", researcher_node)
    builder.add_node("coder", coder_node)
    builder.add_node("browser", browser_node)
    builder.add_node("reporter", reporter_node)

    # Define edges for valid Command.goto destinations.
    builder.add_edge(START, "coordinator")
    builder.add_edge("coordinator", "planner")
    builder.add_edge("coordinator", END)
    builder.add_edge("planner", "supervisor")
    builder.add_edge("planner", END)
    builder.add_edge("supervisor", "researcher")
    builder.add_edge("supervisor", "coder")
    builder.add_edge("supervisor", "browser")
    builder.add_edge("supervisor", "reporter")
    builder.add_edge("supervisor", END)
    builder.add_edge("researcher", "supervisor")
    builder.add_edge("coder", "supervisor")
    builder.add_edge("browser", "supervisor")
    builder.add_edge("reporter", "supervisor")

    return builder.compile()