#!/usr/bin/env python3
"""Build the Ranked Saturday artifact and the weekly email summary.

Usage:
    python3 cfb-matchups/build.py cfb-matchups/data/2026-week02.json

Writes:
    cfb-matchups/dist/index.html   the artifact page (template.html + enriched data)
    cfb-matchups/dist/summary.md   the plain-text weekly summary for email
"""
import json
import sys
from datetime import datetime
from pathlib import Path

HERE = Path(__file__).resolve().parent
LEVEL_POINTS = {"P4": 3, "G5": 1, "FCS": 0}
QUALITY = {"Big Ten", "SEC"}


def rank_map(poll):
    return {team: rank for team, rank in poll["ranks"]}


def tier_for(ra, rb, la, lb):
    """Label a matchup from both teams' ranks (None = unranked) and levels."""
    if ra and rb:
        return "Marquee" if (ra <= 10 or rb <= 10) else "Ranked duel"
    if ra or rb:
        other = lb if ra else la
        if other == "P4":
            return "Power test"
        return "Tune-up"
    if la == "P4" and lb == "P4":
        return "Power matchup"
    return "Light"


def score_for(ra, rb, la, lb):
    def side(r, lvl):
        return (26 - r) if r else LEVEL_POINTS[lvl]
    return side(ra, la) + side(rb, lb)


def enrich(data):
    teams = data["teams"]
    polls = data["polls"]
    maps = {key: rank_map(p) for key, p in polls.items()}
    for g in data["games"]:
        a, h = g["away"], g["home"]
        ta, th = teams[a], teams[h]
        g["away_conf"], g["home_conf"] = ta["conf"], th["conf"]
        g["away_level"], g["home_level"] = ta["level"], th["level"]
        g["conference_game"] = ta["conf"] == th["conf"] and ta["conf"] != "Independent"
        g["quality_conf"] = ta["conf"] in QUALITY or th["conf"] in QUALITY
        g["ranks"] = {}
        g["tier"] = {}
        g["score"] = {}
        for key, m in maps.items():
            ra, rh = m.get(a), m.get(h)
            g["ranks"][key] = {"away": ra, "home": rh}
            g["tier"][key] = tier_for(ra, rh, ta["level"], th["level"])
            g["score"][key] = score_for(ra, rh, ta["level"], th["level"])
        g.setdefault("status", "scheduled")
        g.setdefault("note", "")
        g.setdefault("tv", "TBA")
        dt = datetime.strptime(g["date"], "%Y-%m-%d")
        g["day"] = dt.strftime("%a")
        g["date_label"] = dt.strftime("%A, %b %-d")
    # This week's opponent for every ranked team, for the poll table.
    opp = {}
    for g in data["games"]:
        opp[g["away"]] = {"opponent": g["home"], "at": True, "date": g["date"], "time_et": g["time_et"], "tv": g["tv"]}
        opp[g["home"]] = {"opponent": g["away"], "at": False, "date": g["date"], "time_et": g["time_et"], "tv": g["tv"]}
    data["this_week"] = opp
    data["default_poll"] = "cfp" if polls["cfp"]["ranks"] else "ap"
    return data


def fmt_time(t):
    h, m = (int(x) for x in t.split(":"))
    suffix = "a.m." if h < 12 else "p.m."
    h12 = h if 1 <= h <= 12 else (h - 12 if h > 12 else 12)
    return f"{h12}:{m:02d} {suffix}" if m else f"{h12} {suffix}"


def summary(data):
    key = data["default_poll"]
    poll = data["polls"][key]
    m = rank_map(poll)
    lines = []
    lines.append(f"Ranked Saturday — {data['week_label']} ({data['window']})")
    lines.append(f"Basis: {poll['name']} released {poll['released']}. {data['basis_note']}")
    lines.append("")

    def label(t):
        r = m.get(t)
        return f"No. {r} {t}" if r else t

    def line(g):
        sep = "vs." if g.get("neutral") else "at"
        core = f"{label(g['away'])} {sep} {label(g['home'])}"
        when = f"{g['day']} {fmt_time(g['time_et'])} ET, {g['tv']}"
        extra = f" — {g['result']}" if g.get("result") else ""
        return f"- {core} · {when}{extra}"

    games = sorted(data["games"], key=lambda g: (g["date"], g["time_et"]))
    marquee = [g for g in games if g["ranks"][key]["away"] and g["ranks"][key]["home"]]
    lines.append(f"RANKED vs. RANKED ({len(marquee)})")
    lines.extend(line(g) for g in marquee) if marquee else lines.append("- none this week")
    lines.append("")
    top25 = [g for g in games if (g["ranks"][key]["away"] or g["ranks"][key]["home"]) and g not in marquee]
    lines.append(f"OTHER TOP 25 GAMES ({len(top25)})")
    lines.extend(line(g) for g in top25)
    lines.append("")
    qc = [g for g in games if g["quality_conf"] and not (g["ranks"][key]["away"] or g["ranks"][key]["home"])]
    lines.append(f"BIG TEN + SEC, UNRANKED ({len(qc)})")
    lines.extend(line(g) for g in qc)
    lines.append("")
    lines.append("TOP 25 THIS WEEK (" + poll["name"] + ")")
    lines.append(", ".join(f"{r} {t}" for t, r in poll["ranks"]))
    if data.get("notes"):
        lines.append("")
        lines.append("Notes")
        lines.extend(f"- {n}" for n in data["notes"])
    return "\n".join(lines) + "\n"


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    data = enrich(json.loads(Path(sys.argv[1]).read_text()))
    template = (HERE / "template.html").read_text()
    payload = json.dumps(data, separators=(",", ":")).replace("</", "<\\/")
    html = template.replace("__DATA_JSON__", payload)
    out = HERE / "dist"
    out.mkdir(exist_ok=True)
    (out / "index.html").write_text(html)
    (out / "summary.md").write_text(summary(data))
    print(f"wrote {out/'index.html'} ({len(html):,} bytes) and {out/'summary.md'}")


if __name__ == "__main__":
    main()
