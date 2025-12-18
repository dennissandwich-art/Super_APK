# Super_APK_Structure.md  (Canonical)

main.py                -> UI entrypoint (boot-first)
app_kernel.py          -> Core logic (deterministic)
feature_flags.py       -> Feature gating (env-aware)
kernel_state.py        -> State container
kernel_health.py       -> Health snapshot
error_boundary.py      -> Error containment
safe_logger.py         -> In-memory logging
env_gate.py            -> Build-time env access
ui_*                   -> UI-only modules
persistence_*          -> Persistence abstraction (safe default)

payments/*             -> OPTIONAL, ISOLATED (other branch)
analysis/*             -> NON-RUNTIME (other branch)
