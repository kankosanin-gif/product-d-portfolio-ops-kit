#!/usr/bin/env python3
import datetime as dt
import subprocess
from pathlib import Path

try:
    import tomllib
except Exception:
    tomllib = None

ROOT = Path('/Users/Antares/.openclaw/workspace/kuro-agent-org-public')
OUT = ROOT / 'agent-org' / 'reports' / 'hourly-status.md'


def run(cmd, cwd=ROOT):
    try:
        p = subprocess.run(cmd, cwd=str(cwd), capture_output=True, text=True, timeout=20)
        return p.returncode, p.stdout.strip(), p.stderr.strip()
    except Exception as e:
        return 1, '', str(e)


def detect_hook_config_source():
    toml_path = ROOT / 'agent-org' / 'hooks' / 'hooks.toml'
    json_path = ROOT / 'agent-org' / 'hooks' / 'hooks.json'
    if toml_path.exists() and tomllib is not None:
        return 'hooks.toml'
    if json_path.exists():
        return 'hooks.json'
    return 'none'


def main():
    now = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S %Z')

    rc1, gs_out, _ = run(['git', 'status', '--short'])
    rc2, lg_out, _ = run(['git', 'log', '--oneline', '-n', '3'])

    summary = 'OK'
    if rc1 != 0 or rc2 != 0:
        summary = 'WARN: git check failed'

    hook_src = detect_hook_config_source()

    lines = []
    lines.append(f'# Hourly Report — {now}')
    lines.append('')
    lines.append(f'- Topline: **{summary}**')
    lines.append('- Emergency: **None**')
    lines.append(f'- Hook Config Source: **{hook_src}**')
    lines.append('')
    lines.append('## Git Working Tree')
    lines.append('```')
    lines.append(gs_out or '(clean)')
    lines.append('```')
    lines.append('')
    lines.append('## Recent Commits')
    lines.append('```')
    lines.append(lg_out or '(no commits)')
    lines.append('```')
    lines.append('')
    lines.append('## Next')
    lines.append('- Continue portfolio-first execution plan')
    lines.append('- Maintain boundary/security controls')

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text('\n'.join(lines), encoding='utf-8')

    run(['python3', str(ROOT / 'agent-org' / 'hooks' / 'run_hooks.py')])


if __name__ == '__main__':
    main()
