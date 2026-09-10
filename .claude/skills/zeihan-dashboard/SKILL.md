---
name: zeihan-dashboard
description: >-
  Generate or refresh "The Zeihan Lens" — a self-contained HTML geopolitical dashboard with a
  world map and per-country briefs that read consumers, demographics, capital, energy, food and
  trade exposure through Peter Zeihan's deglobalization framework, with 2025→2050 forecasts for
  25 major economies. Use this skill whenever the user asks for a geopolitical dashboard, a
  demographics dashboard, a Zeihan-style or "end of globalization" view, country outlooks or
  forecasts by country, a world map of demographic or economic trends, who wins and loses from
  deglobalization, aging/consumer/capital cohort comparisons across countries, or wants to add,
  remove or re-score countries on a previously generated Zeihan Lens — even if they don't say
  "dashboard" or "Zeihan" explicitly. Also use when asked to refresh the page with newer UN or
  IMF figures.
---

# The Zeihan Lens

Build one self-contained HTML page (no build step, no runtime libraries; the world map paths are
already inlined) that shows how major economies fare as the post-1945 trade order unwinds, in
Peter Zeihan's reading. The page opens in any browser and publishes cleanly as an Artifact.

The template already contains a complete, working dashboard for 25 countries. Most requests are
edits to its data block, not a rebuild. Preserve the page's structure and design; change the data.

## What the page contains

- **World map** (Equal Earth) colored by a selectable metric: Zeihan outlook, trajectory,
  30–44 prime-consumer change, 45–64 capital-rich change, working-age change, median age,
  fertility, household consumption share, export dependence. Hover for values, click for a brief.
- **Country brief**: outlook meter, a Zeihan-style take, population / median age / fertility /
  GDP tiles, 2025 vs 2050 age-structure chart, seven trend checks, watch items.
- **Trajectory board**: Rising / Holding / Fading / Breaking groups.
- **Sortable table** across every metric.
- **Framework notes** and a data-caveat footer.

## Workflow

### 1. Decide the country set and the scope of change

Read the request. Three common shapes:

- *"Make the dashboard"* — use the template as-is with a quick data sanity pass (step 3).
- *"Add / remove / focus on countries"* — edit the `C` array (step 2). Any country in the
  Natural Earth 110m set can be added; `references/data-model.md` lists ISO numeric ids for the
  likely candidates. Keep the set to roughly 20–35: the map labels and the table stay readable.
- *"Refresh with the latest figures"* — web-search the UN World Population Prospects (latest
  revision, medium variant) and the IMF World Economic Outlook for each country and update the
  fields. Record the vintage in the masthead `.meta` block. Never invent a number: if a figure
  can't be found, keep the previous value and say so in your reply.

### 2. Edit the data block

Copy `assets/dashboard_template.html` to your working location, then edit the `const C = [...]`
array in its `<script>`. Each entry is one country; the fields, units and scoring rubric are in
`references/data-model.md` — read it before writing a new entry, because the outlook score and
the `take` are what make the page Zeihan's view rather than a generic demographics page.

Two rules that keep the derived numbers honest:

- The five age-band shares in `b25` and `b50` must each sum to 100. The 30–44, 45–64 and
  15–64 changes on the page are computed from these bands times the population figures, so a
  typo here silently corrupts three metrics.
- The `id` must be the zero-padded ISO 3166-1 numeric code as a string (`'076'` for Brazil).
  The map colors countries by matching this id against the inlined path data.

If you add a country whose label would collide with neighbours (small European or Gulf states,
Korea/Japan), add an absolute label position to the `ABS` map in the script; otherwise the label
is placed at the country's centroid.

### 3. Validate

Run the bundled check on the edited file:

```bash
node scripts/check_data.mjs path/to/dashboard.html
```

It parses the `C` array and reports band sums that miss 100, ids missing from the map data,
values outside plausible ranges (fertility, median age, shares), and countries with no `take`
or empty `risks`. Fix anything it flags before delivering; the script is the difference between a
page that quietly shows a wrong cohort change and one that is right.

### 4. Deliver

- **Artifact available** (Claude Code / claude.ai): publish the file with the Artifact tool. The
  template is already artifact-shaped (title, styles and body, no `<!doctype>` wrapper) and
  themes itself to the viewer's light or dark setting. Keep the favicon `🗺️` and the title
  "The Zeihan Lens" on redeploys so the user's gallery entry stays stable.
- **File delivery only**: prepend
  `<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">`
  and save as `zeihan_lens.html`, then present it.

In the accompanying message, give a two-to-three sentence read of the board (who is Rising, who
is Breaking, and the one or two countries whose scores would be most contested), and note that
the outlooks are an editorial synthesis of Zeihan's public commentary rather than his figures or
a consensus forecast. Readers deserve to know the page presents one analyst's framework.

## Design notes (only if the user asks for visual changes)

The page follows a briefing-chart aesthetic: Barlow Condensed for display and eyebrows, Public
Sans for body, IBM Plex Mono for figures; a cool slate ground; blue↔red diverging ramps with a
grey midpoint for signed metrics, a single blue ramp for magnitudes, and a four-hue trajectory
palette (blue / green / amber / red) validated for color-vision deficiency in both themes. All
colors are CSS custom properties at the top of the `<style>` block; change tokens there rather
than in components so both themes stay consistent. Status meaning always carries a label or
glyph as well as a color.
