"""Workflow service for managing agent workflow execution."""

import asyncio
from typing import AsyncGenerator, Dict, List

from langchain_core.messages import HumanMessage, AIMessage

from src.workflow.graph import build_graph


def _to_langchain_messages(messages: List[Dict[str, str]]):
    result = []
    for m in messages:
        if m["role"] == "user":
            result.append(HumanMessage(content=m["content"]))
        else:
            result.append(AIMessage(content=m["content"]))
    return result


async def run_agent_workflow(
    messages: List[Dict[str, str]], debug: bool = False
) -> AsyncGenerator[Dict[str, str], None]:
    """Run the agent workflow with the given messages.

    Args:
        messages: List of chat messages
        debug: Whether to enable debug logging

    Yields:
        Event data for SSE streaming
    """
    workflow = build_graph()
    langchain_messages = _to_langchain_messages(messages)

    # LangGraph astream yields dicts keyed by node name, e.g.:
    # {"coordinator": {"messages": [AIMessage(...)], "next": "planner"}}
    async for event in workflow.astream({"messages": langchain_messages}):
        for node_name, node_output in event.items():
            if not isinstance(node_output, dict):
                continue
            node_messages = node_output.get("messages", [])
            if not node_messages:
                continue
            last_msg = node_messages[-1]
            content = last_msg.content if hasattr(last_msg, "content") else str(last_msg)
            if content:
                yield {
                    "event": "message",
                    "data": {"content": content, "role": "assistant", "node": node_name},
                }
        await asyncio.sleep(0.05)