#!/usr/bin/env python3
"""Refresh the embedded 2026 schedule from ESPN and report what the league moved.

    python3 scripts/update_schedule.py           # rewrite index.html + sunday-wall.html
    python3 scripts/update_schedule.py --check   # report changes only, write nothing

Pulls every regular-season week from ESPN's public scoreboard API, keeps the
Sunday 1:00 ET and 4:05/4:25 ET games plus any game whose kickoff is not set yet
(flex), and replaces the JSON in the `#sked` script tag of both pages. Thursday,
Sunday night, Monday, international and holiday games are left out.

Exits 0 when nothing changed, 1 when the schedule changed (and was written,
unless --check), 2 on a fetch or parse error, so a scheduled job can tell them apart.
"""
import json
import re
import sys
import time
import urllib.request
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parent.parent
PAGES = [ROOT / "index.html", ROOT / "sunday-wall.html"]
SEASON = "2026"
WEEKS = 18
URL = ("https://site.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard"
       "?dates={season}&seasontype=2&week={week}")
ET = ZoneInfo("America/New_York")
SKED = re.compile(r'(<script id="sked" type="application/json">)(.*?)(</script>)', re.S)
SLATES = {"13:00": "early", "16:05": "late", "16:25": "late"}
NETS = {"Fox": "FOX"}
ORDER = {"early": 0, "late": 1, "tbd": 2}


def fetch(week):
    url = URL.format(season=SEASON, week=week)
    for attempt in range(5):
        try:
            with urllib.request.urlopen(url, timeout=30) as r:
                return json.load(r)
        except Exception as e:  # ESPN drops the odd connection; back off and retry
            if attempt == 4:
                raise RuntimeError(f"week {week}: {e}") from e
            time.sleep(2 ** (attempt + 1))


def game(event):
    c = event["competitions"][0]
    side = {x["homeAway"]: x["team"]["abbreviation"] for x in c["competitors"]}
    kick = datetime.fromisoformat(event["date"].replace("Z", "+00:00")).astimezone(ET)
    g = {"id": event["id"], "away": side["away"], "home": side["home"],
         "slate": "tbd", "time": "", "net": "",
         "date": kick.strftime("%Y-%m-%d"), "venue": c["venue"]["fullName"]}
    if c.get("timeValid", True):
        slate = SLATES.get(kick.strftime("%H:%M"))
        if kick.weekday() != 6 or not slate:
            return None
        nets = [n for b in c.get("broadcasts", []) for n in b.get("names", [])]
        g.update(slate=slate, time=kick.strftime("%-I:%M %p"),
                 net=NETS.get(nets[0], nets[0]) if nets else "")
    return g


def build(teams):
    weeks = []
    for n in range(1, WEEKS + 1):
        games = [g for g in map(game, fetch(n)["events"]) if g]
        # 1:00 window, then 4:05 before 4:25, then flex; alphabetical by visitor within each
        games.sort(key=lambda g: (ORDER[g["slate"]], g["time"], g["away"]))
        sunday = next((g["date"] for g in games if g["slate"] != "tbd"),
                      games[0]["date"] if games else None)
        label = datetime.strptime(sunday, "%Y-%m-%d").strftime("%b %-d") if sunday else ""
        weeks.append({"week": n, "date": label, "games": games})
    return {"season": SEASON, "teams": teams, "weeks": weeks}


def describe(g):
    when = f'{g["time"]} {g["net"]}'.strip() if g["slate"] != "tbd" else "Flex (time TBD)"
    return f'{g["away"]} @ {g["home"]} — {g["date"]} {when}'


def changes(old, new):
    out = []
    for ow, nw in zip(old["weeks"], new["weeks"]):
        o = {g["id"]: g for g in ow["games"]}
        n = {g["id"]: g for g in nw["games"]}
        for i in n.keys() - o.keys():
            out.append(f'Week {nw["week"]}: added   {describe(n[i])}')
        for i in o.keys() - n.keys():
            out.append(f'Week {ow["week"]}: removed {describe(o[i])} (moved out of the Sunday windows)')
        for i in o.keys() & n.keys():
            if o[i] != n[i]:
                out.append(f'Week {nw["week"]}: changed {describe(o[i])}  ->  {describe(n[i])}')
        if ow["date"] != nw["date"]:
            out.append(f'Week {nw["week"]}: date {ow["date"]} -> {nw["date"]}')
    return sorted(out, key=lambda s: int(s.split()[1].rstrip(":")))


def main():
    check = "--check" in sys.argv[1:]
    text = PAGES[0].read_text()
    old = json.loads(SKED.search(text).group(2))
    try:
        new = build(old["teams"])
    except Exception as e:
        print(f"Could not refresh the schedule: {e}", file=sys.stderr)
        return 2
    diff = changes(old, new)
    if not diff:
        print("Schedule unchanged.")
        return 0
    print(f"{len(diff)} schedule change(s):")
    print("\n".join("  " + d for d in diff))
    if not check:
        blob = json.dumps(new, separators=(",", ":"))
        for page in PAGES:
            src = page.read_text()
            page.write_text(SKED.sub(lambda m: m.group(1) + blob + m.group(3), src, count=1))
        total = sum(len(w["games"]) for w in new["weeks"])
        print(f"Wrote {total} games to " + ", ".join(p.name for p in PAGES))
    return 1


if __name__ == "__main__":
    sys.exit(main())
