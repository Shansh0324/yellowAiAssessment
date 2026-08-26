# SOLUTION

## Architecture & Design
The system uses a single FastAPI deployment containing modular services (`OrderService`, `PolicyService`, `ReturnService`, `ExchangeService`, `EscalationService`).
This logical microservices approach enables clear boundaries and testability while avoiding the operational overhead of actual distributed microservices.

## Orchestration & Guardrails
The LLM is tightly restricted through `tool_schemas.py` and the system prompt (`system.md`). The LLM does not perform business logic. It only requests tools, and the Python backend returns deterministic results. If a user asks a policy question, the agent searches the static markdown policy file. It does not invent rules.

## State Management
A `ConversationService` maintains an in-memory dictionary of session contexts (messages and tool calls) to enable multi-turn conversations.

## Failure Handling
The orchestrator limits the LLM to a maximum of 8 tool calls per turn to prevent infinite loops. If an error occurs during tool execution, a structured JSON error string is passed back to the LLM so it can respond gracefully or escalate.

## Trade-offs
- In-memory session state is used to simplify the deployment for this exercise. A production system would use Redis or PostgreSQL.
- The `policy_service` simply returns the entire markdown file content for search. While fine for a small file, a larger knowledge base would require RAG.
