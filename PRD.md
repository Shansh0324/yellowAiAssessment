# Trendly Agentic Support Assistant PRD

## 1. Product Objective
Build an agentic customer-support system for Trendly that handles order lookup, policy questions, return/exchange eligibility, case escalation, and maintains multi-turn conversation state securely and deterministically without hallucination.

## 2. Core Principles
* **LLM Role**: Acts strictly as a reasoning and orchestration layer.
* **Deterministic Services**: All business rules, facts, and action results must come from predefined tools and domain services. The LLM must not invent policy, order data, refund statuses, or any internal identifiers.

## 3. Technology Stack
* Backend: Python 3.11+, FastAPI, Pydantic, Uvicorn
* AI: OpenRouter, Free-tier function-calling model (OpenAI-compatible)
* Frontend: Next.js, React, TypeScript, Tailwind CSS
* Data Source: Fixed `orders.json` and `trendly_policy.md` files.

## 4. Key Features
* **Order Lookup**: Retrieve and explain order status based on ID.
* **Policy Grounding**: Answer policy questions exclusively based on `trendly_policy.md`. Fall back to escalation if the answer isn't in the policy.
* **Return/Exchange Elegibility**: Execute logic using static order data and deterministic rules to process valid returns and size exchanges.
* **Security & Guardrails**: Prevent prompt injections, reject unauthorized discounts, and protect customer data.
* **Failure Handling**: Graceful recovery from tool and LLM timeouts. Strict infinite loop prevention (max 8 tool calls).
* **Multi-turn Context**: Maintain contextual awareness across user prompts within a session.

## 5. Scope
* Logical microservices deployed in a single FastAPI application.
* API Gateway serving `/health`, `/api/v1/chat`, and session endpoints.
* Extensive test coverage (Unit, Integration, Multi-turn, Edge Cases).
