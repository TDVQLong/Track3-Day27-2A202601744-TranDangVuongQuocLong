import json
from typing import TypedDict, Optional
from datetime import datetime
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver

from models import AuditEntry

class GraphState(TypedDict):
    customer_id: str
    proposed_action: str
    confidence_score: float
    reasoning: str
    human_decision: Optional[str]

def evaluate_customer(state: GraphState) -> GraphState:
    # Mock behavior
    return state

def execute_low_risk_action(state: GraphState) -> GraphState:
    return state

def execute_high_risk_action(state: GraphState) -> GraphState:
    return state

def log_audit(state: GraphState) -> GraphState:
    entry = AuditEntry(
        timestamp=datetime.now().isoformat(),
        agent_id="langgraph_agent",
        action=state["proposed_action"],
        confidence=state["confidence_score"],
        reviewer_id="human_reviewer" if state.get("human_decision") else None,
        decision=state.get("human_decision", "auto-approved")
    )
    
    try:
        with open("audit_log.json", "r") as f:
            log_data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        log_data = []
        
    log_data.append(entry.model_dump())
    
    with open("audit_log.json", "w") as f:
        json.dump(log_data, f, indent=4)
        
    return state

def route_action(state: GraphState) -> str:
    action = state["proposed_action"]
    confidence = state["confidence_score"]
    
    if action == "increase_credit_limit":
        return "execute_high_risk_action"
    
    if confidence >= 0.85:
        return "execute_low_risk_action"
        
    return "execute_high_risk_action"


workflow = StateGraph(GraphState)

workflow.add_node("evaluate_customer", evaluate_customer)
workflow.add_node("execute_low_risk_action", execute_low_risk_action)
workflow.add_node("execute_high_risk_action", execute_high_risk_action)
workflow.add_node("log_audit", log_audit)

workflow.add_edge(START, "evaluate_customer")

workflow.add_conditional_edges(
    "evaluate_customer",
    route_action,
    {
        "execute_low_risk_action": "execute_low_risk_action",
        "execute_high_risk_action": "execute_high_risk_action"
    }
)

workflow.add_edge("execute_low_risk_action", "log_audit")
workflow.add_edge("execute_high_risk_action", "log_audit")
workflow.add_edge("log_audit", END)

memory = MemorySaver()
app = workflow.compile(checkpointer=memory, interrupt_before=["execute_high_risk_action"])
