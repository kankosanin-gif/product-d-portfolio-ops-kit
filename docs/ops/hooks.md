# Hook Automation (Local)

## Purpose
Run lightweight automatic actions after hourly audits.

## Components
- Config: `agent-org/hooks/hooks.json`
- Runner: `agent-org/hooks/run_hooks.py`
- Trigger source: `agent-org/scripts/hourly_audit.py`
- Action queue output: `agent-org/reports/action-queue.md`

## Current hooks
1. `dirty-working-tree`
   - Trigger: hourly report contains changed/untracked files
   - Action: append actionable item to action queue

2. `warn-topline`
   - Trigger: hourly report topline contains WARN
   - Action: append escalation item to action queue

## Execution
Hourly audit now automatically calls hook runner.
Manual run:
```bash
python3 /Users/Antares/.openclaw/workspace/agent-org/hooks/run_hooks.py
```

## Notes
- Local-only execution under `/Users/Antares`
- No external messaging or secret output
- Dedup per hour via `agent-org/reports/hook-state.log`
