# ui_login.py
# BRANCH: main
# ROLE: Telegram Login UI (EARLY PHASE, MINIMUM)

"""
LOGIN UI SPEC:
- One button: "Login med Telegram"
- Status text (empty / error / success)
- 5 states: Idle, Logging in, Success, Fail, Backend down

NO:
- Graphics
- Loading spinners
- Animations
"""

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label


class LoginState:
    IDLE = "idle"
    LOGGING_IN = "logging_in"
    SUCCESS = "success"
    FAIL = "fail"
    BACKEND_DOWN = "backend_down"


class LoginScreen(BoxLayout):
    def __init__(self, on_login_request=None, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"
        self.padding = 40
        self.spacing = 20

        self._on_login_request = on_login_request
        self._state = LoginState.IDLE

        # App title
        self._title = Label(
            text="Super_APK",
            font_size="32sp",
            size_hint=(1, 0.3)
        )
        self.add_widget(self._title)

        # Status label
        self._status = Label(
            text="",
            font_size="16sp",
            size_hint=(1, 0.2)
        )
        self.add_widget(self._status)

        # Login button
        self._login_btn = Button(
            text="Login med Telegram",
            font_size="20sp",
            size_hint=(1, 0.3)
        )
        self._login_btn.bind(on_press=self._on_login_press)
        self.add_widget(self._login_btn)

        # Spacer
        self.add_widget(Label(size_hint=(1, 0.2)))

    def _on_login_press(self, instance):
        if self._state == LoginState.LOGGING_IN:
            return  # Prevent double-tap
        if self._on_login_request:
            self._on_login_request()

    def set_state(self, state: str):
        """Update UI based on state."""
        self._state = state

        if state == LoginState.IDLE:
            self._status.text = ""
            self._login_btn.disabled = False

        elif state == LoginState.LOGGING_IN:
            self._status.text = "Logger ind..."
            self._login_btn.disabled = True

        elif state == LoginState.SUCCESS:
            self._status.text = "Login godkendt"
            self._login_btn.disabled = True

        elif state == LoginState.FAIL:
            self._status.text = "Adgang afvist"
            self._login_btn.disabled = False

        elif state == LoginState.BACKEND_DOWN:
            self._status.text = "Login utilgængeligt"
            self._login_btn.disabled = False
