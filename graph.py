from typing import TypedDict
from langgraph.graph import StateGraph, END
from states import (
    parse_with_llm,
    check_availability,
    check_conflict,
    llm_agent,
    confirm_and_book,
)


# --------- State Schema ---------

class BookingState(TypedDict, total=False):
    request: str
    parsed: bool
    room: str
    day: str
    time: str
    persons: int
    room_available: bool
    user_busy: bool
    confirmed: bool
    llm_response: str
    status: str
    error: str


# --------- Build LangGraph Workflow ---------

workflow = StateGraph(BookingState)

workflow.add_node("ParseWithLLM", parse_with_llm.run)
workflow.add_node("CheckAvailability", check_availability.run)
workflow.add_node("CheckConflict", check_conflict.run)
workflow.add_node("LLMAgent", llm_agent.run)
workflow.add_node("ConfirmAndBook", confirm_and_book.run)

workflow.set_entry_point("ParseWithLLM")

workflow.add_edge("ParseWithLLM", "CheckAvailability")
workflow.add_edge("CheckAvailability", "CheckConflict")
workflow.add_edge("CheckConflict", "LLMAgent")
workflow.add_edge("LLMAgent", "ConfirmAndBook")
workflow.add_edge("ConfirmAndBook", END)

graph = workflow.compile(debug=True)


def run_graph(user_input):
    if isinstance(user_input, str):
        state = {"request": user_input}
    else:
        state = user_input

    result = graph.invoke(state)
    return result
