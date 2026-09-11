# Ranked Saturday — weekly FBS matchup board

Generates a private Claude artifact that lists the week's college football
games involving Top 25 teams (all conferences) or Big Ten / SEC teams, with
poll ranks from the AP Top 25 and the US LBM Coaches Poll, and from the CFP
rankings once the committee releases them (first release: Tue Nov 3, 2026).

## Layout

- `data/2026-weekNN.json` — one file per week: polls, team conference/level
  lookup, and the game list (ET kickoff, TV, note, result).
- `template.html` — the page. `__DATA_JSON__` is replaced at build time.
- `build.py` — enriches the data (ranks per poll, matchup tier, quality score,
  each ranked team's game this week) and writes `dist/index.html` plus
  `dist/summary.md` (the plain-text weekly email).

```
python3 cfb-matchups/build.py cfb-matchups/data/2026-week02.json
```

`dist/` is generated and not committed.

## Weekly refresh (Thursdays)

A scheduled Routine spins up a fresh session each Thursday morning that:

1. checks out this branch,
2. collects the newest AP and Coaches polls (and CFP rankings from Nov 3 on)
   and the Thursday–Saturday schedule for ranked and Big Ten/SEC teams,
3. writes the new `data/2026-weekNN.json`, runs `build.py`,
4. republishes the existing artifact in place (same link), and
5. sends the summary by email.

Direct HTTP to ESPN, NCAA.com, CBS Sports and similar hosts is blocked by
the session's egress policy, so the data is gathered with web search and
cross-checked (for example, ranked-team counts per conference).

## Data conventions

- `level`: `P4` (Big Ten, SEC, ACC, Big 12, Notre Dame), `G5` (other FBS,
  including the 2026 Pac-12 and UConn), `FCS`.
- Matchup quality: sum of (26 − rank) for each ranked team; an unranked team
  adds 3 (P4), 1 (G5) or 0 (FCS). Tiers: Marquee (both ranked, one top 10),
  Ranked duel, Power test, Tune-up, Power matchup, Light.
- Tied poll slots repeat the rank number. `polls.coaches.inferred` lists
  teams whose exact slot was placed by elimination rather than confirmed.
- Times are Eastern, 24-hour `HH:MM`.
