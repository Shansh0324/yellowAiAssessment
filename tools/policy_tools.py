from services.policy.service import PolicyService

policy_service = PolicyService()

def search_policy(query: str) -> str:
    """Search the store policy for answers to customer questions."""
    return policy_service.search_policy(query)
