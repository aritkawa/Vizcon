# Data Sources & References — The World's Most Diligent Insomniacs

All sources are publicly accessible. Links verified 2026-07-31.
出典はすべて一般公開・アクセス可能。リンクは2026-07-31確認。

---

## Primary dataset (backbone of all 7 acts)

**OECD Time Use Database** — minutes/day by activity, ages 15–64, whole population.
The single coordinate system used across the entire piece (work / commute / sleep / unpaid work, all on the same ruler).
- https://www.oecd.org/en/data/datasets/time-use-database.html
- OECD Data Explorer (Time use): https://data-explorer.oecd.org/vis?df[ds]=DisseminateFinalDMZ&df[id]=DSD_TIME_USE@DF_TIME_USE&df[ag]=OECD.WISE.INE
- Coverage: 33 countries; each country is its most recent survey between **1998–2019** (time-use surveys run only every 10–15 years, so this is not a single-year snapshot).

**Japan's snapshot (2016)** — Statistics Bureau of Japan, *Survey on Time Use and Leisure Activities* (社会生活基本調査).
- Outline (EN): https://www.stat.go.jp/english/data/shakai/2016/gaiyo.html
- Data (e-Stat, EN): https://www.e-stat.go.jp/en/statistics/00200533

---

## The Rebuttal act (labour statistics — a series separate from time-use diaries)

**Share of employed working 49+ hours per week** — ILO, via JILPT *Databook of International Labour Statistics 2025*, Table 6-3. 22 countries with 2023 data.
The "49 hours" threshold = exceeding the 48-hour standard week of **ILO Convention No. 1 (1919)**, the internationally agreed definition of long working hours.
- JILPT Databook 2025: https://www.jil.go.jp/english/estatis/databook/index2025.html
- ILOSTAT (Japan country profile): https://ilostat.ilo.org/data/country-profiles/jpn/

**Annual working hours per worker (2023)** — Penn World Table, via Our World in Data.
- https://ourworldindata.org/grapher/annual-working-hours-per-worker
- Context page: https://ourworldindata.org/working-hours

---

## The Prescription act (sleep science)

**Pre-sleep warm bath / passive body heating** — Haghayegh S. et al. (2019). "Before-bedtime passive body heating by warm shower or bath to improve sleep: A systematic review and meta-analysis." *Sleep Medicine Reviews*, 46, 124–135.
- DOI / ScienceDirect: https://www.sciencedirect.com/science/article/pii/S1087079218301552
- PubMed: https://pubmed.ncbi.nlm.nih.gov/31102877/

**Caffeine timing before bed** — Drake C. et al. (2013). "Caffeine effects on sleep taken 0, 3, or 6 hours before going to bed." *Journal of Clinical Sleep Medicine*, 9(11), 1195–1200.
- DOI: https://doi.org/10.5664/jcsm.3170
- PubMed / open full text: https://pmc.ncbi.nlm.nih.gov/articles/PMC3805807/

---

## Notes on definitions & handling (stated in-page)

- "Work" is a whole-population, 7-day average — it includes weekends and people not in employment, so it reads lower than a full-timer's gut feeling.
- Country totals are normalized to exactly **1,440 minutes** to absorb source rounding.
- Time-use (diary-based) measurement and annual-working-hour labour statistics use **different definitions and are different series**; the piece keeps them separate and says so wherever both appear.
- "Unpaid work" = chores, shopping, child & adult care, and volunteering combined.

---

## Hosting & AI concierge (technical references, not data sources)

- Public hosting: **GitHub Pages** (primary) — https://aritkawa.github.io/diligent-insomniacs/ ; mirror: Streamlit — https://diligent-insomniacs.streamlit.app/
- AI concierge: **Groq** LLM (llama-3.3-70b) grounded only in on-page data, with a deterministic in-browser fallback.
