
from typing import Any, TypedDict

from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, START, StateGraph

from app.agent_loop import run_agent


class AgentState(TypedDict, total=False):
    question: str
    animal_profile: dict | None
    approved: bool
    needs_approval: bool
    answer: str
    tool: str
    tool_result: Any
    history: list


VACCINE_KEYWORDS = [
    "vaccine",
    "vaccination",
    "booster",
    "fmd",
    "brucellosis",
    "theileriosis",
    "लसीकरण",
    "लस",
    "लसी",
]


def detect_node(state: AgentState):
    question = state.get("question", "")
    history = state.get("history", [])

    is_vaccine_request = any(
        keyword in question.lower()
        for keyword in VACCINE_KEYWORDS
    )

    # Save the question in conversation memory
    if not history or history[-1].get("question") != question:
        history.append({
            "question": question
        })

    return {
        "needs_approval": is_vaccine_request,
        "history": history
    }


def approval_node(state: AgentState):
    return {
        "answer": (
            "Vaccination scheduler वापरण्यापूर्वी confirmation आवश्यक आहे. "
            "तुम्हाला दिलेल्या animal details नुसार vaccination dates "
            "calculate करायच्या आहेत का? कृपया approved=True देऊन confirm करा."
        ),
        "tool": "approval_required"
    }


def execute_node(state: AgentState):
    question = state.get("question", "")
    animal_profile = state.get("animal_profile")

    history = state.get("history", [])

    # Include recent conversation context
    previous_context = ""

    for item in history[-4:-1]:
        previous_context += (
            f"Previous question: {item.get('question', '')}\n"
            f"Previous answer: {item.get('answer', '')}\n"
        )

    contextual_question = question

    if previous_context:
        contextual_question = (
            f"Conversation context:\n{previous_context}\n"
            f"Current question: {question}"
        )

    result = run_agent(
        contextual_question,
        animal_profile=animal_profile
    )

    answer = result.get("answer", result.get("message", "No response"))

    history.append({
        "question": question,
        "answer": answer
    })

    return {
        "answer": answer,
        "tool": result.get("tool"),
        "tool_result": result.get("tool_result"),
        "history": history
    }


def route_after_detection(state: AgentState):
    if state.get("needs_approval") and not state.get("approved", False):
        return "approval"

    return "execute"


# Build graph
workflow = StateGraph(AgentState)

workflow.add_node("detect", detect_node)
workflow.add_node("approval", approval_node)
workflow.add_node("execute", execute_node)

workflow.add_edge(START, "detect")

workflow.add_conditional_edges(
    "detect",
    route_after_detection,
    {
        "approval": "approval",
        "execute": "execute"
    }
)

workflow.add_edge("approval", END)
workflow.add_edge("execute", END)

# Memory checkpoint
memory = MemorySaver()

graph = workflow.compile(checkpointer=memory)


def run_graph(
    question,
    animal_profile=None,
    approved=False,
    thread_id="pashuseva-user"
):
    config = {
        "configurable": {
            "thread_id": thread_id
        }
    }

    result = graph.invoke(
        {
            "question": question,
            "animal_profile": animal_profile,
            "approved": approved
        },
        config=config
    )

    return result
