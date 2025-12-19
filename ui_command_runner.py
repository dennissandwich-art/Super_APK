# ui_command_runner.py
# BRANCH: main
# ROLE: UI command runner (SAFE)

class UICommandRunner:
    def run(self, command):
        try:
            command.execute()
        except Exception as e:
            print("Command failed:", e)
