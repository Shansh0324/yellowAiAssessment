from domain.escalation import Escalation
from datetime import datetime, timezone
import uuid

class EscalationService:
    def escalate_case(self, session_id: str, customer_id: str, reason: str, summary: str, actions_taken: list[str], order_id: str = None) -> Escalation:
        esc = Escalation(
            escalation_id=f"ESC-{uuid.uuid4().hex[:6].upper()}",
            session_id=session_id,
            customer_id=customer_id,
            order_id=order_id,
            reason=reason,
            summary=summary,
            actions_taken=actions_taken,
            created_at=datetime.now(timezone.utc),
            status="open"
        )
        # In a real system, you would save this to a database or send an email/webhook
        return esc
