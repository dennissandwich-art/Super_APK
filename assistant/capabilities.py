# assistant/capabilities.py
# BRANCH: main
# ROLE: AI Assistant capabilities registry

"""
CAPABILITIES:
- Define what the assistant CAN do
- Each capability is validated before execution
- Extensible through registration
"""

from typing import Dict, List, Callable, Any


class AssistantCapabilities:
    """
    Registry of assistant capabilities.
    """

    def __init__(self):
        self._capabilities: Dict[str, Dict] = {}
        self._register_default_capabilities()

    def _register_default_capabilities(self):
        """Register built-in capabilities."""

        # System capabilities
        self.register("system.status", self._get_system_status, {
            "description": "Get system status",
            "admin_only": False
        })

        self.register("system.checkup", self._run_checkup, {
            "description": "Run system checkup",
            "admin_only": False
        })

        # Data capabilities
        self.register("data.validate", self._validate_data, {
            "description": "Validate data",
            "admin_only": False
        })

        self.register("data.consolidate", self._consolidate_data, {
            "description": "Consolidate data sources",
            "admin_only": False
        })

        # Research capabilities
        self.register("research.web", self._web_research, {
            "description": "Perform web research",
            "admin_only": False
        })

        self.register("research.analyze", self._analyze_research, {
            "description": "Analyze research results",
            "admin_only": False
        })

        # Admin capabilities
        self.register("admin.users", self._manage_users, {
            "description": "Manage users",
            "admin_only": True
        })

        self.register("admin.config", self._manage_config, {
            "description": "Manage configuration",
            "admin_only": True
        })

        self.register("admin.logs", self._view_logs, {
            "description": "View system logs",
            "admin_only": True
        })

    def register(self, name: str, handler: Callable, metadata: Dict = None):
        """Register a capability."""
        self._capabilities[name] = {
            "handler": handler,
            "metadata": metadata or {}
        }

    def execute(self, name: str, params: Dict = None) -> Dict:
        """Execute a capability."""
        if name not in self._capabilities:
            return {"status": "error", "reason": f"Unknown capability: {name}"}

        try:
            handler = self._capabilities[name]["handler"]
            result = handler(params or {})
            return {"status": "ok", "result": result}
        except Exception as e:
            return {"status": "error", "reason": str(e)}

    def list_all(self) -> List[Dict]:
        """List all capabilities."""
        return [
            {
                "name": name,
                "description": cap["metadata"].get("description", ""),
                "admin_only": cap["metadata"].get("admin_only", False)
            }
            for name, cap in self._capabilities.items()
        ]

    def is_admin_only(self, name: str) -> bool:
        """Check if capability requires admin."""
        if name not in self._capabilities:
            return True  # Unknown = restricted
        return self._capabilities[name]["metadata"].get("admin_only", False)

    # ==================
    # DEFAULT HANDLERS
    # ==================

    def _get_system_status(self, params: Dict) -> Dict:
        return {"status": "operational"}

    def _run_checkup(self, params: Dict) -> Dict:
        return {"checks_passed": True}

    def _validate_data(self, params: Dict) -> Dict:
        data = params.get("data")
        return {"valid": data is not None}

    def _consolidate_data(self, params: Dict) -> Dict:
        sources = params.get("sources", [])
        return {"consolidated": True, "source_count": len(sources)}

    def _web_research(self, params: Dict) -> Dict:
        topic = params.get("topic", "")
        return {"topic": topic, "results": []}

    def _analyze_research(self, params: Dict) -> Dict:
        return {"analysis": "pending"}

    def _manage_users(self, params: Dict) -> Dict:
        return {"action": params.get("action"), "status": "ok"}

    def _manage_config(self, params: Dict) -> Dict:
        return {"config": "ok"}

    def _view_logs(self, params: Dict) -> Dict:
        return {"logs": []}
