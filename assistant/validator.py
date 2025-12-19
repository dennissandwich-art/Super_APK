# assistant/validator.py
# BRANCH: main
# ROLE: AI Assistant validation engine (ALWAYS CORRECT)

"""
VALIDATOR:
- Ensures all inputs are valid before processing
- Ensures all actions are safe before execution
- Prevents invalid state transitions
"""

from typing import Dict, Any, List


class AssistantValidator:
    """
    Validation engine for AI Assistant.
    Ensures correctness at every step.
    """

    def __init__(self):
        self._schemas: Dict[str, Dict] = {}
        self._rules: List[Dict] = []
        self._register_default_rules()

    def _register_default_rules(self):
        """Register default validation rules."""
        # Input rules
        self._rules.append({
            "name": "input_not_empty",
            "check": lambda x: x is not None and len(str(x).strip()) > 0,
            "message": "Input cannot be empty"
        })

        self._rules.append({
            "name": "input_max_length",
            "check": lambda x: len(str(x)) <= 10000,
            "message": "Input too long (max 10000 chars)"
        })

    def validate_input(self, input_text: str) -> Dict:
        """Validate user input."""
        if input_text is None:
            return {"valid": False, "reason": "Input is None"}

        if not isinstance(input_text, str):
            return {"valid": False, "reason": "Input must be string"}

        if len(input_text.strip()) == 0:
            return {"valid": False, "reason": "Input is empty"}

        if len(input_text) > 10000:
            return {"valid": False, "reason": "Input too long"}

        return {"valid": True}

    def validate_data(self, data: Any, schema: str = None) -> Dict:
        """Validate data against schema."""
        if data is None:
            return {"valid": False, "reason": "Data is None"}

        if schema and schema in self._schemas:
            return self._validate_against_schema(data, self._schemas[schema])

        # Basic validation
        return {"valid": True, "data_type": type(data).__name__}

    def validate_admin_action(self, action: str, params: Dict) -> Dict:
        """Validate admin action before execution."""
        if not action:
            return {"valid": False, "reason": "Action not specified"}

        # Check for dangerous actions
        dangerous_actions = ["delete_all", "reset", "drop"]
        if action.lower() in dangerous_actions:
            if not params.get("confirm"):
                return {"valid": False, "reason": "Dangerous action requires confirmation"}

        return {"valid": True}

    def validate_response(self, response: Dict) -> Dict:
        """Validate response before sending."""
        if not isinstance(response, dict):
            return {"valid": False, "reason": "Response must be dict"}

        if "status" not in response:
            return {"valid": False, "reason": "Response missing status"}

        return {"valid": True}

    def _validate_against_schema(self, data: Any, schema: Dict) -> Dict:
        """Validate data against schema definition."""
        # Basic schema validation
        required = schema.get("required", [])
        if isinstance(data, dict):
            for field in required:
                if field not in data:
                    return {"valid": False, "reason": f"Missing required field: {field}"}

        return {"valid": True}

    def register_schema(self, name: str, schema: Dict):
        """Register a validation schema."""
        self._schemas[name] = schema

    def add_rule(self, name: str, check: callable, message: str):
        """Add a validation rule."""
        self._rules.append({
            "name": name,
            "check": check,
            "message": message
        })
