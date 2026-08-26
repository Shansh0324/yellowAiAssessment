AGENT_TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_order",
            "description": "Retrieve details for a specific order by order_id.",
            "parameters": {
                "type": "object",
                "properties": {
                    "order_id": {"type": "string", "description": "The order ID, e.g., TR-4530"},
                    "customer_id": {"type": "string", "description": "The customer ID"}
                },
                "required": ["order_id", "customer_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_customer_orders",
            "description": "Retrieve a list of all recent orders for a specific customer. Use this when the user asks about their latest order or doesn't provide an order ID.",
            "parameters": {
                "type": "object",
                "properties": {
                    "customer_id": {"type": "string", "description": "The customer ID"}
                },
                "required": ["customer_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "search_policy",
            "description": "Search the store policy for answers to customer questions.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "The customer's question or search query"}
                },
                "required": ["query"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "check_return_eligibility",
            "description": "Check if an item in an order is eligible for return.",
            "parameters": {
                "type": "object",
                "properties": {
                    "order_id": {"type": "string", "description": "The order ID"},
                    "customer_id": {"type": "string", "description": "The customer ID"},
                    "item_id": {"type": "string", "description": "The item ID to check"}
                },
                "required": ["order_id", "customer_id", "item_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "create_return",
            "description": "Create a return request for eligible items.",
            "parameters": {
                "type": "object",
                "properties": {
                    "order_id": {"type": "string", "description": "The order ID"},
                    "customer_id": {"type": "string", "description": "The customer ID"},
                    "items_to_return": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "item_id": {"type": "string"},
                                "quantity": {"type": "integer"},
                                "reason": {"type": "string"}
                            },
                            "required": ["item_id", "quantity", "reason"]
                        }
                    }
                },
                "required": ["order_id", "customer_id", "items_to_return"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "escalate_to_human",
            "description": "Escalate the current conversation to a human support agent.",
            "parameters": {
                "type": "object",
                "properties": {
                    "session_id": {"type": "string"},
                    "customer_id": {"type": "string"},
                    "reason": {"type": "string"},
                    "summary": {"type": "string"},
                    "actions_taken": {
                        "type": "array",
                        "items": {"type": "string"}
                    },
                    "order_id": {"type": "string"}
                },
                "required": ["session_id", "customer_id", "reason", "summary", "actions_taken"]
            }
        }
    }
]
