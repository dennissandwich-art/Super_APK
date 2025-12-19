# ui_login_result.py
# BRANCH: main
# ROLE: Login result screen (EARLY PHASE)

"""
RESULT SCREEN SPEC:
- Shows "Login succesfuldt" or error message
- No navigation in early phase
"""

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label


class LoginResultScreen(BoxLayout):
    def __init__(self, success: bool = True, message: str = None, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"
        self.padding = 40
        self.spacing = 20

        # Title
        self._title = Label(
            text="Super_APK",
            font_size="32sp",
            size_hint=(1, 0.3)
        )
        self.add_widget(self._title)

        # Result message
        if message:
            result_text = message
        elif success:
            result_text = "Login succesfuldt"
        else:
            result_text = "Adgang afvist"

        self._result = Label(
            text=result_text,
            font_size="20sp",
            size_hint=(1, 0.4)
        )
        self.add_widget(self._result)

        # Spacer
        self.add_widget(Label(size_hint=(1, 0.3)))
