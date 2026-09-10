# Data model and scoring rubric

## Country entry

Each element of `const C = [...]` in the template:

```js
{id:'484', name:'Mexico', region:'North America',
 pop:[131,144],            // millions, [2025, 2050 forecast]
 age:30.5,                 // median age, years (2025)
 tfr:1.8,                  // total fertility rate, births per woman
 gdp:1.9,                  // nominal GDP, USD trillions (values < 1 render as billions)
 pc:14.5,                  // GDP per capita, USD thousands
 gr:1.0,                   // real GDP growth, % (latest year)
 cons:68,                  // household consumption, % of GDP
 exp:36,                   // exports of goods and services, % of GDP
 b25:[23.5,24.5,22,21.5,8.5],   // 2025 age-band shares, % — must sum to 100
 b50:[17,19,21,27,16],          // 2050 age-band shares, % — must sum to 100
 energy:'balanced',        // 'exporter' | 'balanced' | 'importer'  (net position)
 food:'importer',          // 'exporter' | 'balanced' | 'importer'  (net calories)
 outlook:8,                // 1–10, see rubric
 traj:'rising',            // 'rising' | 'stable' | 'fading' | 'collapsing'
 take:'Two to four sentences in Zeihan's framing.',
 risks:['Cartel violence','Water and power']}
```

Fields the page derives (do not add them by hand): working-age change `wa`, prime-consumer change
`consumers`, capital-rich change `capital`, 65+ share in 2050 `old50`, population change `popChg`.

## Age bands and what they mean in Zeihan's framework

| Band | Role on the page | Why it matters |
|---|---|---|
| 0–14 | Dependents | Cost now, workers in 15 years; tells you the fertility story |
| 15–29 | Entrants | Labor supply, little capital, first-time consumers |
| 30–44 | Prime consumers | Homes, cars, children: the demand engine of a consumption-led economy |
| 45–64 | Capital-rich | Peak savings and investment; retire and the cheap capital goes with them |
| 65+ | Retirees | Drawdown of savings, higher state costs, labor shortage |

Approximate bands from the UN World Population Prospects (latest revision, medium variant) age
tables; round to the nearest 0.5. When only 0–14 / 15–64 / 65+ are handy, split 15–64 using the
country's median age as a guide (young countries put more in 15–29; old countries in 45–64).

## Outlook score rubric (1–10)

Score the country as Zeihan has described it in his books (*The Accidental Superpower*, *The
Absent Superpower*, *Disunited Nations*, *The End of the World Is Just the Beginning*) and his
talks and newsletters. Weigh, in roughly this order:

1. **Demographic runway** — size of the 30–44 and 45–64 cohorts now and in 2050; fertility.
2. **Trade model** — consumption-led (insulated) versus export-led (exposed).
3. **Energy and food** — net exporter, self-sufficient, or dependent on sea-borne imports.
4. **Geography and security** — continental market, ocean moat, navy, US alliance, chokepoints.
5. **Capital access** — domestic savings versus dependence on foreign capital.

| Score | Reading | Examples in the default set |
|---|---|---|
| 9–10 | Insulated and gaining; Zeihan's clear winners | United States (9) |
| 7–8 | Rising, with a real constraint he names | Mexico (8), Australia (8), India (7), Turkey (7), Indonesia (7), Canada (7) |
| 5–6 | Holding through managed decline or commodity strength | Japan (5), France (6), Brazil (6), Argentina (6), Vietnam (6), Saudi Arabia (5), UK (5) |
| 3–4 | Fading: aging or exposed, decline expected | Germany (3), Spain (3), Poland (4), South Korea (3), Iran (3), Egypt (3), Nigeria (4), South Africa (4) |
| 1–2 | A system he expects to break within a generation | China (1), Russia (2), Italy (2) |

Trajectory follows the score with judgment: `rising` 7–10 (or 6 with clear momentum, as
Argentina and Vietnam), `stable` 5–7 with resources or alliances that cushion decline,
`fading` 3–5, `collapsing` 1–3 where Zeihan has explicitly forecast systemic failure. The
trajectory is what the board and the pills show, so be deliberate about the boundary cases.

## Writing the take

Two to four sentences, in the voice of a briefing summarizing Zeihan, not Zeihan himself. Name
the mechanism he cites (aging cohort, lost gas supply, sea-lane dependence, shale, NAFTA), the
outcome he forecasts, and the constraint or caveat he acknowledges. Avoid hedged generic
statements: "faces demographic challenges" says nothing; "its last large cohort retires in the
2030s and nothing follows it" is the framework doing work. Do not invent quotes.

Watch items (`risks`) are two to four short noun phrases the reader should track.

## ISO numeric ids for likely additions

All of these exist in the inlined map data. Ids are strings, zero-padded to three characters.

| Country | id | Country | id | Country | id |
|---|---|---|---|---|---|
| Netherlands | 528 | Ukraine | 804 | Pakistan | 586 |
| Sweden | 752 | Kazakhstan | 398 | Bangladesh | 050 |
| Norway | 578 | Israel | 376 | Thailand | 764 |
| Switzerland | 756 | UAE | 784 | Philippines | 608 |
| Austria | 040 | Iraq | 368 | Malaysia | 458 |
| Belgium | 056 | Jordan | 400 | Taiwan | 158 |
| Denmark | 208 | Syria | 760 | Myanmar | 104 |
| Finland | 246 | Yemen | 887 | North Korea | 408 |
| Greece | 300 | Algeria | 012 | Mongolia | 496 |
| Hungary | 348 | Morocco | 504 | Afghanistan | 004 |
| Portugal | 620 | Libya | 434 | Colombia | 170 |
| Romania | 642 | Sudan | 729 | Chile | 152 |
| Czechia | 203 | Ethiopia | 231 | Peru | 604 |
| New Zealand | 554 | Kenya | 404 | Venezuela | 862 |
| Papua New Guinea | 598 | Tanzania | 834 | Ecuador | 218 |
| Cuba | 192 | Uganda | 800 | Bolivia | 068 |
| Guatemala | 320 | Ghana | 288 | Paraguay | 600 |
| DR Congo | 180 | Cameroon | 120 | Uruguay | 858 |
| Zimbabwe | 716 | | | | |

The default 25: United States 840, Canada 124, Mexico 484, Brazil 076, Argentina 032,
United Kingdom 826, France 250, Germany 276, Italy 380, Spain 724, Poland 616, Russia 643,
Turkey 792, Saudi Arabia 682, Iran 364, Egypt 818, Nigeria 566, South Africa 710, India 356,
China 156, Japan 392, South Korea 410, Indonesia 360, Vietnam 704, Australia 036.

## Map labels

Labels default to the country centroid plus an offset from the `LABELS` map (`[dx, dy]` in the
1000×520 viewBox). Crowded countries use an absolute position from the `ABS` map instead. When
adding a small country near others, add an `ABS` entry; place the label over sea or over a
country that is not in the set, and keep it to one short word (the label text is the country
name unless the script shortens it: USA, UK, Saudi, S. Africa, Korea).

## Sources and vintages

- Demographics: UN World Population Prospects, medium variant (2024 revision at time of writing;
  use the latest). Bands, median age, fertility, 2050 population.
- Economics: IMF World Economic Outlook (GDP, per capita, growth); World Bank WDI (household
  consumption and exports as % of GDP). Round to the precision shown in the template.
- Energy and food positions: net trade balance in energy (IEA, EIA) and in food calories
  (FAO). Zeihan's own characterization wins ties; he is the framework being presented.

Update the masthead `.meta` lines when the vintage changes so readers can see what they are
looking at.
