# assistant/__init__.py
# BRANCH: main
# ROLE: AI Assistant package

from assistant.core import AIAssistant
from assistant.capabilities import AssistantCapabilities
from assistant.validator import AssistantValidator
from assistant.research import ResearchEngine
from assistant.consolidator import DataConsolidator
from assistant.admin_panel import AdminPanel

__all__ = [
    "AIAssistant",
    "AssistantCapabilities",
    "AssistantValidator",
    "ResearchEngine",
    "DataConsolidator",
    "AdminPanel"
]
