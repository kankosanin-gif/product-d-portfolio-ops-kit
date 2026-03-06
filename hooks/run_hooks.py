#!/usr/bin/env python3
import json
from datetime import datetime
from pathlib import Path

try:
    import tomllib  # py311+
except Exception:
    tomllib = None

ROOT = Path('/Users/Antares/.openclaw/workspace/kuro-agent-org-public')


def read_text(rel):
    p = ROOT / rel
    if not p.exists():
        return ''
    return p.read_text(encoding='utf-8', errors='ignore')


def append_markdown(rel, title, body):
    p = ROOT / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    ts = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with p.open('a', encoding='utf-8') as f:
        f.write(f"\n## [{ts}] {title}\n{body}\n")


def already_fired(rel, hook_id, stamp):
    p = ROOT / rel
    if not p.exists():
        return False
    txt = p.read_text(encoding='utf-8', errors='ignore')
    return f"{hook_id}:{stamp}" in txt


def mark_fired(rel, hook_id, stamp):
    p = ROOT / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open('a', encoding='utf-8') as f:
        f.write(f"{hook_id}:{stamp}\n")


def load_hooks_config():
    cfg_json = ROOT / 'agent-org/hooks/hooks.json'
    cfg_toml = ROOT / 'agent-org/hooks/hooks.toml'

    if cfg_toml.exists() and tomllib is not None:
        return tomllib.loads(cfg_toml.read_text(encoding='utf-8')), 'hooks.toml'
    if cfg_json.exists():
        return json.loads(cfg_json.read_text(encoding='utf-8')), 'hooks.json'
    return {'hooks': []}, 'none'


def main():
    cfg, _ = load_hooks_config()
    state_path = 'agent-org/reports/hook-state.log'
    hooks = cfg.get('hooks', [])

    for h in hooks:
        if not h.get('enabled', True):
            continue

        trigger = h.get('when', {})
        if trigger.get('type') != 'contains':
            continue

        rel = trigger.get('file')
        base_text = read_text(rel)
        if not base_text:
            continue

        must_contain = trigger.get('text', '')
        if must_contain and must_contain not in base_text:
            continue

        any_list = h.get('if_any', [])
        if any_list and not any(t in base_text for t in any_list):
            continue

        stamp = datetime.now().strftime('%Y-%m-%d-%H')
        hook_id = h.get('id', 'unknown')
        if already_fired(state_path, hook_id, stamp):
            continue

        act = h.get('action', {})
        if act.get('type') == 'append_markdown':
            append_markdown(
                act.get('file', 'agent-org/reports/action-queue.md'),
                f"HOOK:{hook_id}",
                act.get('body', '')
            )
            mark_fired(state_path, hook_id, stamp)


if __name__ == '__main__':
    main()
