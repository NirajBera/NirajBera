#!/usr/bin/env python3
"""Builds dist/telemetry.svg (monochrome stats card) from the GitHub GraphQL API."""
import json, os, datetime as dt, urllib.request
from xml.sax.saxutils import escape as esc

USER = os.environ.get("GH_USER", "NirajBera")
Q = """query($login:String!){user(login:$login){followers{totalCount}
 repositories(ownerAffiliations:OWNER,privacy:PUBLIC,first:100){totalCount nodes{stargazerCount}}
 contributionsCollection{totalCommitContributions totalPullRequestContributions
  contributionCalendar{totalContributions weeks{contributionDays{date contributionCount}}}}}}"""


def fetch():
    fx = os.environ.get("FIXTURE")
    if fx:
        return json.load(open(fx))
    req = urllib.request.Request("https://api.github.com/graphql", data=json.dumps({"query": Q, "variables": {"login": USER}}).encode(),
                                 headers={"Authorization": "bearer " + os.environ["GH_TOKEN"], "Content-Type": "application/json"})
    return json.load(urllib.request.urlopen(req))


u = fetch()["data"]["user"]
cc = u["contributionsCollection"]
cal = cc["contributionCalendar"]
days = [d for w in cal["weeks"] for d in w["contributionDays"]]
today = dt.datetime.now(dt.timezone.utc).date().isoformat()
days = [d for d in days if d["date"] <= today]
counts = [d["contributionCount"] for d in days]
# streaks
longest = cur = 0
for c in counts:
    cur = cur + 1 if c else 0
    longest = max(longest, cur)
i = len(counts) - 1
if i >= 0 and counts[i] == 0:
    i -= 1
current = 0
while i >= 0 and counts[i]:
    current += 1
    i -= 1
stars = sum(n["stargazerCount"] for n in u["repositories"]["nodes"])
last30 = counts[-30:]
mx = max(last30 + [1])

W, H = 900, 330
FONT = "Inter,'Segoe UI',system-ui,-apple-system,Roboto,Helvetica,Arial,sans-serif"
MONO = "'JetBrains Mono','SF Mono',Consolas,'DejaVu Sans Mono',monospace"
tiles = [("CONTRIBUTIONS", cal["totalContributions"], "last 12 months"), ("CURRENT STREAK", current, "days"),
         ("LONGEST STREAK", longest, "days, this year"), ("PUBLIC REPOS", u["repositories"]["totalCount"], f"{stars} stars · {u['followers']['totalCount']} followers")]
s = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}"><style>'
     f'text{{font-family:{FONT}}}.m{{font-family:{MONO}}}'
     '.bar{transform-box:fill-box;transform-origin:bottom;animation:g 1.1s cubic-bezier(.2,.8,.2,1) both}'
     '@keyframes g{from{transform:scaleY(0)}to{transform:scaleY(1)}}'
     '.bl{animation:bl 1s steps(1) infinite}@keyframes bl{50%{opacity:0}}'
     '.pop{animation:p .7s ease-out both}@keyframes p{from{opacity:0;transform:translateY(8px)}to{opacity:1;transform:none}}</style>')
tw = (W - 3 * 14) / 4
for k, (lab, val, sub) in enumerate(tiles):
    x = k * (tw + 14)
    s += (f'<g class="pop" style="animation-delay:{k * .12:.2f}s"><rect x="{x:.0f}" y="0" width="{tw:.0f}" height="124" rx="14" fill="#0d0d0d" stroke="#262626"/>'
          f'<text x="{x + 20:.0f}" y="30" font-size="11" fill="#8a8a8a" font-weight="700" letter-spacing="1.4">{lab}</text>'
          f'<text x="{x + 20:.0f}" y="82" font-size="44" fill="#ffffff" font-weight="800">{val}</text>'
          f'<text x="{x + 20:.0f}" y="108" font-size="12" fill="#8a8a8a">{esc(sub)}</text></g>')
s += '<rect x="0" y="138" width="900" height="192" rx="14" fill="#0d0d0d" stroke="#262626"/>'
s += '<text x="20" y="168" font-size="11" fill="#8a8a8a" font-weight="700" letter-spacing="1.4">LAST 30 DAYS</text>'
bw = (W - 40 - 29 * 6) / 30
for k, c in enumerate(last30):
    h = 6 + (c / mx) * 100 if c else 3
    x = 20 + k * (bw + 6)
    shade = "#ffffff" if c else "#2a2a2a"
    s += f'<rect class="bar" x="{x:.1f}" y="{300 - h:.1f}" width="{bw:.1f}" height="{h:.1f}" rx="3" fill="{shade}" style="animation-delay:{k * .03:.2f}s"/>'
    if c:
        s += f'<text x="{x + bw / 2:.1f}" y="{294 - h:.1f}" font-size="9" fill="#bdbdbd" text-anchor="middle">{c}</text>'
upd = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
s += f'<text class="m" x="880" y="168" font-size="10" fill="#6a6a6a" text-anchor="end">live · updated {upd}</text>'
s += f'<text class="m" x="20" y="320" font-size="10" fill="#6a6a6a">{days[-30]["date"] if len(days) >= 30 else ""}</text><text class="m" x="880" y="320" font-size="10" fill="#6a6a6a" text-anchor="end">{days[-1]["date"]}</text></svg>'
os.makedirs("dist", exist_ok=True)
open("dist/telemetry.svg", "w", encoding="utf-8").write(s)
print("telemetry ok", cal["totalContributions"], current, longest)
