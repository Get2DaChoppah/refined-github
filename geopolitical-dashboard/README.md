# The Zeihan Lens

A self-contained HTML dashboard (`index.html`, no build step, no runtime dependencies) that reads 25 major economies through Peter Zeihan's demographics-and-deglobalization framework.

- **World map** (Equal Earth, inlined from Natural Earth 110m via `world-atlas`) colored by a selectable metric: Zeihan outlook, trajectory, 30–44 prime-consumer cohort change, 45–64 capital-rich cohort change, working-age change, median age, fertility, household consumption share, export dependence.
- **Country brief** for the selected country: outlook meter, Zeihan-style take, population / median age / fertility / GDP tiles, 2025 vs 2050 age-structure chart, seven trend checks (consumers, capital, workforce, retiree load, energy, food, trade exposure) and watch items.
- **Trajectory board** grouping the set into Rising / Holding / Fading / Breaking.
- **Sortable country table** across all metrics.

Data notes: demographic figures are rounded approximations of the UN World Population Prospects 2024 medium variant; economic figures approximate IMF WEO and World Bank 2024–25. Cohort changes are computed from the age bands in the file. The outlook scores and takes are an editorial synthesis of Zeihan's public commentary, not his numbers and not an endorsement.

Open `index.html` directly in a browser. Fonts load from Google Fonts when online and fall back to system faces otherwise.
