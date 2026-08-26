from services.escalation.service import EscalationService
import json

escalation_service = EscalationService()

def escalate_to_human(session_id: str, customer_id: str, reason: str, summary: str, actions_taken: list[str], order_id: str = None) -> str:
    """Escalate the current conversation to a human support agent."""
    esc = escalation_service.escalate_case(
        session_id=session_id,
        customer_id=customer_id,
        reason=reason,
        summary=summary,
        actions_taken=actions_taken,
        order_id=order_id
    )
    return esc.model_dump_json()
