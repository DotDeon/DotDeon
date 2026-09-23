"""Render streak-dark.svg and streak-light.svg from the contribution calendar.

Usage:
  GITHUB_TOKEN=... python3 assets/build-streak.py DotDeon out/dir
  python3 assets/build-streak.py DotDeon out/dir --from calendar.json   # offline

The calendar comes from the GraphQL contributionsCollection, which includes
private contribution counts because the profile opts in to showing them.
"""
import datetime as dt
import json
import os
import sys
import urllib.request
from pathlib import Path

QUERY = """{ user(login:"%s"){ contributionsCollection { contributionCalendar {
  totalContributions weeks { contributionDays { date contributionCount } } } } } }"""

PALETTES = {
    "dark": dict(num="#e8e8e8", label="#8f8f8f", line="#5a5a5a"),
    "light": dict(num="#111111", label="#6b6b6b", line="#c8c8c8"),
}


def fetch(user):
    req = urllib.request.Request(
        "https://api.github.com/graphql",
        data=json.dumps({"query": QUERY % user}).encode(),
        headers={"Authorization": f"bearer {os.environ['GITHUB_TOKEN']}",
                 "Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req) as r:
        return json.load(r)


def stats(payload):
    cal = payload["data"]["user"]["contributionsCollection"]["contributionCalendar"]
    days = sorted((d for w in cal["weeks"] for d in w["contributionDays"]), key=lambda d: d["date"])
    today = dt.date.today().isoformat()
    current = 0
    for d in reversed(days):
        if d["contributionCount"] > 0:
            current += 1
        elif d["date"] == today:
            continue          # an empty today does not end a streak yet
        else:
            break
    longest = run = 0
    for d in days:
        run = run + 1 if d["contributionCount"] > 0 else 0
        longest = max(longest, run)
    active = sum(1 for d in days if d["contributionCount"] > 0)
    return dict(total=cal["totalContributions"], current=current, longest=longest, active=active)


def cell(x, value, label, p, delay):
    return f'''  <g class="cell" style="animation-delay:{delay}s">
    <text class="num" x="{x}" y="46" text-anchor="middle">{value}</text>
    <text class="label" x="{x}" y="70" text-anchor="middle">{label}</text>
  </g>'''


def render(s, p):
    cells = [
        (f"{s['total']:,}", "CONTRIBUTIONS"),
        (f"{s['active']}", "ACTIVE DAYS"),
        (f"{s['current']}", "CURRENT STREAK"),
        (f"{s['longest']}", "LONGEST STREAK"),
    ]
    W, n = 760, len(cells)
    col = W / n
    body = "\n".join(cell(round(col * (i + 0.5), 1), v, l, p, round(0.15 + i * 0.12, 2)) for i, (v, l) in enumerate(cells))
    dividers = "\n".join(
        f'  <line class="rule" x1="{round(col * i, 1)}" y1="30" x2="{round(col * i, 1)}" y2="78"/>' for i in range(1, n))
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="96" viewBox="0 0 {W} 96" role="img" aria-label="{s['total']} contributions in the last year, {s['active']} active days, current streak {s['current']} days, longest streak {s['longest']} days">
  <style>
    .num {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
            font-size: 30px; font-weight: 700; letter-spacing: -1px; fill: {p['num']}; }}
    .label {{ font-family: ui-monospace, SFMono-Regular, "SF Mono", Menlo, Consolas, monospace;
              font-size: 10.5px; letter-spacing: 1.8px; fill: {p['label']}; }}
    .rule {{ stroke: {p['line']}; stroke-width: 1; }}
    .cell {{ animation: rise 0.8s cubic-bezier(.2,.8,.2,1) both; }}
    @keyframes rise {{ from {{ opacity: 0; transform: translateY(10px); }} to {{ opacity: 1; transform: none; }} }}
    @media (prefers-reduced-motion: reduce) {{ .cell {{ animation: none; }} }}
  </style>
{dividers}
{body}
</svg>
'''


if __name__ == "__main__":
    user, out = sys.argv[1], Path(sys.argv[2])
    payload = json.load(open(sys.argv[4])) if "--from" in sys.argv else fetch(user)
    s = stats(payload)
    out.mkdir(parents=True, exist_ok=True)
    for name, p in PALETTES.items():
        (out / f"streak-{name}.svg").write_text(render(s, p))
    print(json.dumps(s))
