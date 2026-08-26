class PolicyService:
    def __init__(self, policy_path: str = "data/trendly_policy.md"):
        self.policy_path = policy_path
        self.policy_content = self._load_policy()

    def _load_policy(self) -> str:
        try:
            with open(self.policy_path, "r", encoding="utf-8") as f:
                return f.read()
        except FileNotFoundError:
            return ""

    def search_policy(self, query: str) -> str:
        # In a real app, you might parse sections. 
        # For this exercise with a small markdown file, returning the whole policy 
        # or performing basic keyword extraction works.
        return self.policy_content
