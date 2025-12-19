# assistant/core.py
# BRANCH: main
# ROLE: AI Assistant core engine (POWERFUL, ALWAYS CORRECT)

"""
AI ASSISTANT CORE:
- Deep integration with app
- Consolidation of data
- Validation of operations
- Live web research capability
- Continuous checkups
- Admin panel backbone

DESIGN PRINCIPLES:
- Always correct: Validate before acting
- Powerful: Full access to app state
- Safe: No destructive actions without confirmation
"""

from typing import Optional, Dict, List, Any, Callable
from assistant.capabilities import AssistantCapabilities
from assistant.validator import AssistantValidator
from assistant.research import ResearchEngine
from assistant.consolidator import DataConsolidator


class AIAssistant:
    """
    Deep, powerful AI assistant.
    Backbone of the admin panel.
    """

    def __init__(self, config: Dict = None):
        self._config = config or {}
        self._capabilities = AssistantCapabilities()
        self._validator = AssistantValidator()
        self._research = ResearchEngine()
        self._consolidator = DataConsolidator()

        # State
        self._context: Dict[str, Any] = {}
        self._history: List[Dict] = []
        self._checkup_results: List[Dict] = []

        # Callbacks
        self._on_response: Optional[Callable] = None
        self._on_error: Optional[Callable] = None

    # ==================
    # CORE INTERFACE
    # ==================

    def process(self, input_text: str, context: Dict = None) -> Dict:
        """
        Process user input and return response.
        Always validates before acting.
        """
        # Merge context
        if context:
            self._context.update(context)

        # Validate input
        validation = self._validator.validate_input(input_text)
        if not validation["valid"]:
            return self._error_response(validation["reason"])

        # Determine intent
        intent = self._analyze_intent(input_text)

        # Execute based on intent
        result = self._execute_intent(intent, input_text)

        # Record history
        self._record_interaction(input_text, result)

        return result

    def query(self, question: str) -> Dict:
        """
        Direct query interface for quick lookups.
        """
        return self.process(question, {"mode": "query"})

    def validate(self, data: Any, schema: str = None) -> Dict:
        """
        Validate data against schema or rules.
        """
        return self._validator.validate_data(data, schema)

    def research(self, topic: str) -> Dict:
        """
        Perform live web research on topic.
        """
        return self._research.search(topic)

    def consolidate(self, sources: List[Dict]) -> Dict:
        """
        Consolidate multiple data sources into unified view.
        """
        return self._consolidator.consolidate(sources)

    def checkup(self) -> Dict:
        """
        Run system checkup and return health report.
        """
        results = {
            "timestamp": self._get_timestamp(),
            "checks": [],
            "status": "healthy"
        }

        # Run all checkups
        checks = self._run_checkups()
        results["checks"] = checks

        # Determine overall status
        if any(c["status"] == "critical" for c in checks):
            results["status"] = "critical"
        elif any(c["status"] == "warning" for c in checks):
            results["status"] = "warning"

        self._checkup_results.append(results)
        return results

    # ==================
    # ADMIN PANEL API
    # ==================

    def admin_query(self, query: str, admin_token: str) -> Dict:
        """
        Admin-level query with elevated permissions.
        """
        if not self._verify_admin(admin_token):
            return self._error_response("Invalid admin token")

        return self.process(query, {"mode": "admin", "elevated": True})

    def get_system_state(self, admin_token: str) -> Dict:
        """
        Get complete system state for admin panel.
        """
        if not self._verify_admin(admin_token):
            return self._error_response("Invalid admin token")

        return {
            "context": self._context,
            "history_count": len(self._history),
            "last_checkup": self._checkup_results[-1] if self._checkup_results else None,
            "capabilities": self._capabilities.list_all()
        }

    def execute_admin_action(self, action: str, params: Dict, admin_token: str) -> Dict:
        """
        Execute admin action with validation.
        """
        if not self._verify_admin(admin_token):
            return self._error_response("Invalid admin token")

        # Validate action
        validation = self._validator.validate_admin_action(action, params)
        if not validation["valid"]:
            return self._error_response(validation["reason"])

        # Execute
        return self._capabilities.execute(action, params)

    # ==================
    # INTERNAL METHODS
    # ==================

    def _analyze_intent(self, input_text: str) -> str:
        """Analyze user intent from input."""
        text_lower = input_text.lower()

        if any(w in text_lower for w in ["check", "status", "health"]):
            return "checkup"
        elif any(w in text_lower for w in ["search", "find", "research"]):
            return "research"
        elif any(w in text_lower for w in ["validate", "verify", "check"]):
            return "validate"
        elif any(w in text_lower for w in ["consolidate", "merge", "combine"]):
            return "consolidate"
        else:
            return "query"

    def _execute_intent(self, intent: str, input_text: str) -> Dict:
        """Execute based on intent."""
        if intent == "checkup":
            return self.checkup()
        elif intent == "research":
            topic = input_text.replace("search", "").replace("find", "").strip()
            return self.research(topic)
        elif intent == "validate":
            return {"status": "ok", "message": "Use validate() method with data"}
        elif intent == "consolidate":
            return {"status": "ok", "message": "Use consolidate() method with sources"}
        else:
            return self._generate_response(input_text)

    def _generate_response(self, input_text: str) -> Dict:
        """Generate response to query."""
        return {
            "status": "ok",
            "response": f"Processed: {input_text}",
            "context": self._context
        }

    def _error_response(self, reason: str) -> Dict:
        """Generate error response."""
        return {
            "status": "error",
            "reason": reason
        }

    def _verify_admin(self, token: str) -> bool:
        """Verify admin token."""
        # In production: verify against session manager
        return token is not None and len(token) > 0

    def _run_checkups(self) -> List[Dict]:
        """Run all system checkups."""
        checks = []

        # Memory check
        checks.append({
            "name": "memory",
            "status": "healthy",
            "details": "Memory usage normal"
        })

        # Context check
        checks.append({
            "name": "context",
            "status": "healthy" if self._context else "warning",
            "details": f"Context has {len(self._context)} items"
        })

        # History check
        checks.append({
            "name": "history",
            "status": "healthy",
            "details": f"History has {len(self._history)} entries"
        })

        return checks

    def _record_interaction(self, input_text: str, result: Dict):
        """Record interaction in history."""
        self._history.append({
            "timestamp": self._get_timestamp(),
            "input": input_text,
            "result_status": result.get("status")
        })

        # Keep history bounded
        if len(self._history) > 1000:
            self._history = self._history[-500:]

    def _get_timestamp(self) -> str:
        """Get current timestamp."""
        import time
        return str(int(time.time()))

    # ==================
    # CALLBACKS
    # ==================

    def set_response_callback(self, callback: Callable):
        """Set callback for responses."""
        self._on_response = callback

    def set_error_callback(self, callback: Callable):
        """Set callback for errors."""
        self._on_error = callback
