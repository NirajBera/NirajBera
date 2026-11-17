#!/usr/bin/env python3
"""Builds dist/snake-dark.svg and dist/snake-light.svg: a self-made monochrome snake that sweeps the
contribution grid (zig-zag) and eats the active days. Works even with very few contributions."""
import json, os, urllib.request

USER = os.environ.get("GH_USER", "NirajBera")
Q = """query($login:String!){user(login:$login){contributionsCollection{contributionCalendar{weeks{contributionDays{contributionCount weekday}}}}}}"""


def fetch():
    fx = os.environ.get("FIXTURE")
    if fx:
        return json.load(open(fx))
    req = urllib.request.Request("https://api.github.com/graphql", data=json.dumps({"query": Q, "variables": {"login": USER}}).encode(),
                                 headers={"Authorization": "bearer " + os.environ["GH_TOKEN"], "Content-Type": "application/json"})
    return json.load(urllib.request.urlopen(req))


weeks = fetch()["data"]["user"]["contributionsCollection"]["contributionCalendar"]["weeks"]
grid = [[d["contributionCount"] for d in w["contributionDays"]] for w in weeks]  # grid[col][row]
cols = len(grid)
CS, GAP, PAD = 13, 3, 16
STEP = CS + GAP
W = PAD * 2 + cols * STEP - GAP
H = PAD * 2 + 7 * STEP - GAP
SEG, D = 7, 0.07  # snake length, seconds per cell

# zig-zag path (col 0 down, col 1 up, ...)
order = []
for c in range(cols):
    rows = range(len(grid[c])) if c % 2 == 0 else range(len(grid[c]) - 1, -1, -1)
    for r in rows:
        order.append((c, r))
N = len(order)
T = (N + SEG + 8) * D
cx = lambda c: PAD + c * STEP
cy = lambda r: PAD + r * STEP
mx = max([v for col in grid for v in col] + [1])


def build(dark):
    bg, empty = ("#0b0b0b", "#1e1e1e") if dark else ("#ffffff", "#e6e6e6")
    lv = ["#4a4a4a", "#7a7a7a", "#b0b0b0", "#ffffff"] if dark else ["#bdbdbd", "#8a8a8a", "#4d4d4d", "#000000"]
    snake = "#ffffff" if dark else "#000000"
    s = f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}"><rect width="{W}" height="{H}" rx="6" fill="{bg}"/>'
    for i, (c, r) in enumerate(order):
        v = grid[c][r]
        if v:
            L = lv[min(3, int(v / mx * 3.99))]
            t = i * D / T
            s += (f'<rect x="{cx(c)}" y="{cy(r)}" width="{CS}" height="{CS}" rx="3" fill="{L}">'
                  f'<animate attributeName="fill" dur="{T:.2f}s" repeatCount="indefinite" calcMode="discrete" '
                  f'keyTimes="0;{t:.4f};1" values="{L};{empty};{empty}"/></rect>')
        else:
            s += f'<rect x="{cx(c)}" y="{cy(r)}" width="{CS}" height="{CS}" rx="3" fill="{empty}"/>'
    path = "M" + " L".join(f"{cx(c)} {cy(r)}" for c, r in order)
    for j in range(SEG):
        sz = CS if j else CS + 2
        off = (CS - sz) / 2
        op = 1 - j * 0.09
        s += (f'<rect width="{sz}" height="{sz}" rx="{4 if j == 0 else 3}" fill="{snake}" opacity="{op:.2f}" x="{off}" y="{off}">'
              f'<animateMotion dur="{N * D:.2f}s" repeatCount="indefinite" begin="-{j * D:.2f}s" path="{path}" calcMode="linear"/></rect>')
    return s + '</svg>'


os.makedirs("dist", exist_ok=True)
open("dist/snake-dark.svg", "w").write(build(True))
open("dist/snake-light.svg", "w").write(build(False))
print("snake ok", cols, N)
