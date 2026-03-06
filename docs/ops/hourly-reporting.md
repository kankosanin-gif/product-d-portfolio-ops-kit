# Hourly Reporting — Operations Note

## Purpose
Provide concise, periodic operational visibility without context bloat.

## Reporter
`agent-org/scripts/hourly_audit.py`

## Output
- `agent-org/reports/hourly-status.md`

## Current report structure
1. Topline status
2. Emergency flag
3. Git working tree snapshot
4. Recent commits snapshot
5. Next actions

## Execution options

### Option A — Cron (recommended)
```bash
# every hour
0 * * * * /usr/bin/python3 /Users/Antares/.openclaw/workspace/agent-org/scripts/hourly_audit.py
```

### Option B — Manual trigger
```bash
python3 /Users/Antares/.openclaw/workspace/agent-org/scripts/hourly_audit.py
```

## Governance requirements
- Report must remain concise and action-oriented
- No secret/env leakage in report output
- Topline + emergency indicator must always be present

## Next iteration candidates
- include deployment health checks
- include gate pass/fail summary
- include open blocker count by department
