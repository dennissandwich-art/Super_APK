# ui_admin.py
# BRANCH: main
# ROLE: Admin panel UI (Kivy)

"""
ADMIN PANEL UI:
- AI Assistant interface
- Dashboard view
- System monitoring
- Action execution
"""

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView

from assistant.admin_panel import AdminPanel


class AdminPanelUI(BoxLayout):
    """
    Admin panel UI with AI assistant integration.
    """

    def __init__(self, admin_token: str = None, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"
        self.padding = 20
        self.spacing = 10

        # Initialize admin panel
        self._panel = AdminPanel()
        if admin_token:
            self._panel.authenticate(admin_token)

        # Build UI
        self._build_ui()

    def _build_ui(self):
        """Build the admin panel UI."""

        # Header
        header = Label(
            text="Admin Panel - AI Assistant",
            font_size="24sp",
            size_hint=(1, 0.1)
        )
        self.add_widget(header)

        # Status bar
        self._status = Label(
            text="Ready",
            font_size="14sp",
            size_hint=(1, 0.05)
        )
        self.add_widget(self._status)

        # Response area (scrollable)
        scroll = ScrollView(size_hint=(1, 0.5))
        self._response = Label(
            text="Ask the AI assistant anything...",
            font_size="14sp",
            size_hint_y=None,
            text_size=(None, None),
            halign="left",
            valign="top"
        )
        self._response.bind(texture_size=self._response.setter('size'))
        scroll.add_widget(self._response)
        self.add_widget(scroll)

        # Input area
        self._input = TextInput(
            hint_text="Enter command or question...",
            multiline=False,
            size_hint=(1, 0.1)
        )
        self._input.bind(on_text_validate=self._on_submit)
        self.add_widget(self._input)

        # Button row
        btn_row = BoxLayout(orientation="horizontal", size_hint=(1, 0.1), spacing=10)

        ask_btn = Button(text="Ask", on_press=self._on_ask)
        btn_row.add_widget(ask_btn)

        checkup_btn = Button(text="Checkup", on_press=self._on_checkup)
        btn_row.add_widget(checkup_btn)

        research_btn = Button(text="Research", on_press=self._on_research)
        btn_row.add_widget(research_btn)

        dashboard_btn = Button(text="Dashboard", on_press=self._on_dashboard)
        btn_row.add_widget(dashboard_btn)

        self.add_widget(btn_row)

        # Quick actions
        action_row = BoxLayout(orientation="horizontal", size_hint=(1, 0.1), spacing=10)

        status_btn = Button(text="System Status", on_press=self._on_status)
        action_row.add_widget(status_btn)

        caps_btn = Button(text="Capabilities", on_press=self._on_capabilities)
        action_row.add_widget(caps_btn)

        self.add_widget(action_row)

    def _on_submit(self, instance):
        """Handle input submission."""
        self._on_ask(None)

    def _on_ask(self, instance):
        """Ask the AI assistant."""
        question = self._input.text.strip()
        if not question:
            return

        self._status.text = "Processing..."
        result = self._panel.ask(question)
        self._display_result(result)
        self._input.text = ""

    def _on_checkup(self, instance):
        """Run system checkup."""
        self._status.text = "Running checkup..."
        result = self._panel.checkup()
        self._display_result(result)

    def _on_research(self, instance):
        """Perform research."""
        topic = self._input.text.strip()
        if not topic:
            self._response.text = "Enter a topic to research"
            return

        self._status.text = "Researching..."
        result = self._panel.research(topic)
        self._display_result(result)

    def _on_dashboard(self, instance):
        """Show dashboard."""
        self._status.text = "Loading dashboard..."
        result = self._panel.get_dashboard()
        self._display_result(result)

    def _on_status(self, instance):
        """Get system status."""
        self._status.text = "Getting status..."
        result = self._panel.get_system_state()
        self._display_result(result)

    def _on_capabilities(self, instance):
        """List capabilities."""
        caps = self._panel.get_capabilities()
        text = "CAPABILITIES:\n\n"
        for cap in caps:
            admin = "[ADMIN] " if cap.get("admin_only") else ""
            text += f"{admin}{cap['name']}\n  {cap['description']}\n\n"
        self._response.text = text
        self._status.text = "Ready"

    def _display_result(self, result):
        """Display result in response area."""
        if isinstance(result, dict):
            text = self._format_dict(result)
        else:
            text = str(result)

        self._response.text = text
        self._status.text = "Ready"

    def _format_dict(self, d: dict, indent: int = 0) -> str:
        """Format dict for display."""
        lines = []
        prefix = "  " * indent
        for key, value in d.items():
            if isinstance(value, dict):
                lines.append(f"{prefix}{key}:")
                lines.append(self._format_dict(value, indent + 1))
            elif isinstance(value, list):
                lines.append(f"{prefix}{key}: [{len(value)} items]")
            else:
                lines.append(f"{prefix}{key}: {value}")
        return "\n".join(lines)

    def authenticate(self, token: str) -> bool:
        """Authenticate the panel."""
        result = self._panel.authenticate(token)
        return result.get("authenticated", False)
