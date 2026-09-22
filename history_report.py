"""Report curated fictional history; no mailbox or model calls."""
import json
from collections import defaultdict
from pathlib import Path

HISTORY = Path(__file__).resolve().parent / 'data/synthetic_history.json'

def build_report(records):
    groups = defaultdict(list)
    seen = set()
    for item in records:
        if item.get('synthetic') is not True:
            raise ValueError('This report accepts explicitly synthetic records only')
        if item['id'] in seen:
            continue
        seen.add(item['id'])
        groups[(item['service'], item['asset'], item['location'])].append(item)
    lines = ['# Alder Works: synthetic recurring-issue report', '',
             'Fictional reports, not measured production incidents. Repeated device reports do not establish a shared root cause.', '']
    repeats = sorted(((key, rows) for key, rows in groups.items() if len(rows) > 1), key=lambda pair: (-len(pair[1]), pair[0]))
    if not repeats:
        lines.append('No repeated service/device/location groups.')
    for (service, asset, location), rows in repeats:
        lines += [f'## {service}: {asset} at {location}', '', f'{len(rows)} distinct reports.', '']
        for item in sorted(rows, key=lambda row: row['reported_at']):
            lines += [f"- {item['id']} | {item['reported_at']} | {item['scope']} | Reported error: {item['error']}",
                      f"  Observations: {'; '.join(item['observations'])}",
                      f"  Performed actions: {'; '.join(item['actions_performed']) or 'None recorded'}. Outcome: {item['outcome']}."]
        lines += ['', 'Vendor handoff: verify timestamps, exact errors, affected workstations, device/application/driver versions, recent changes, attempted checks and observed outcomes. Ask the device owner before any changes. Cause remains unconfirmed.', '']
    return '\n'.join(lines)

if __name__ == '__main__':
    print(build_report(json.loads(HISTORY.read_text(encoding='utf-8'))))
