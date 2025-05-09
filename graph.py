from typing import TypedDict
from langgraph.graph import StateGraph, END
from states import llm_agent, confirm_and_book

# --------- State Schema ---------

class BookingState(TypedDict, total=False):
    request: str
    llm_response: str
    room: str
    day: str
    time: str
    persons: int
    confirmed: bool
    error: str
    status: str

# --------- Build LangGraph Workflow ---------

workflow = StateGraph(BookingState)

workflow.add_node("LLMAgent", llm_agent.run)
workflow.add_node("ConfirmAndBook", confirm_and_book.run)

workflow.set_entry_point("LLMAgent")
workflow.add_edge("LLMAgent", "ConfirmAndBook")
workflow.add_edge("ConfirmAndBook", END)

graph = workflow.compile(debug=True)

def run_graph(user_input):
    if isinstance(user_input, str):
        state = {"request": user_input}
    else:
        state = user_input

    result = graph.invoke(state)
    return result  # Return full state, not just a string

