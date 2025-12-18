# analysis/runtime_surface.py
# BRANCH: claude-analyze-super-apk
# ROLE: Runtime surface documentation

SURFACE = {
    "UI": ["main.py", "ui_*"],
    "KERNEL": ["app_kernel.py", "kernel_*"],
    "DATA": ["feature_flags.py", "env_gate.py"],
    "OPTIONAL": ["payments/*"],
    "ANALYSIS": ["analysis/*"],
}

def run():
    print("RUNTIME SURFACE")
    for layer, files in SURFACE.items():
        print(layer, "->", files)

if __name__ == "__main__":
    run()
