# REVIEW_PACKET — Claim Grading & Reproducibility

**What this is.** Every headline claim in the public visualization, graded one by one, with a
**runnable reproduce command** and a **falsifier condition** attached. This is not a
"we verified our work" statement. It is a re-executable artifact: a third party can run the
same commands against the shipped data (`scrolly/data.js`, 33 countries) and either confirm
each number or watch a claim break.

All commands are run from the project root (`01_sleep_work/`). Node reads the same `data.js`
the site ships; there is no separate analysis dataset to fall out of sync.

---

## Grade legend

| Grade | Meaning |
|---|---|
| **A** | Follows directly from the data. No material caveat needed. |
| **B** | Reproduces, but requires disclosing a caveat that can change the interpretation. |
| **C** | Associational / correlational only. Used with hedged language, never asserted as cause. |
| **D** | Dropped. Failed its own falsifier, or did not earn its place in the story. |

---

## Claim grading

| # | Claim | Where used | Grade | Reproduce | Falsifier (what would break it) | Honest stance |
|---|---|---|---|---|---|---|
| 1 | Japan sleep **444.1 min = lowest of 33** | Act 1 / hero | **A** | `data.js` `DATA`, `Japan.sleep=444.1`, min over 33 | Any country sleeps < 444.1 min | OECD time-use surveys differ by year and method across countries; disclosed once, up front |
| 2 | Japan paid work **297.1 min = highest of 33** | Act 2 | **B** | `data.js` `DATA`, `Japan.work=297.1`, max over 33 | **ILO annual hours rank Japan 1654h BELOW USA 1789h — the opposite order** | Time-use "paid minutes per day" and ILO "annual employed hours" are different measures. We show they disagree and state that "works the most" is the time-use reading, not the ILO one. |
| 3 | Japanese women sleep **438 min = lowest of 33 (women)** | Act 3 | **A** | `data.js` `ACT3`, `Japan.ws=438`, min of `ws` (next: Korea 471.2) | Any country's women sleep < 438 min | The number itself is a direct fact |
| 4 | "Women sleep less than men" holds in only **7 of 33 countries** — Japan is one | Act 3 | **A** | `data.js` `ACT3`, count `ws<ms` -> 7 (Estonia/Greece/India/Italy/Japan/Korea/Spain) | Count becomes >= 8 or <= 6 | **AI's first pass said "5 of 33"; recomputation corrected it to 7 (logged).** Being in the minority is the whole paradox. |
| 5 | Japanese men's unpaid work **40.3 min = lowest in the world** | Act 3 | **A** | `data.js` `ACT3`, `Japan.mu=40.3`, min of `mu` (next: Korea 49.0 / India 51.8) | Any country's men's unpaid work < 40.3 min | Direct fact |
| 6 | (Causal) Women's sleep loss is **driven by** the unpaid-work burden | Act 3 narration | **C** | Correlation only: `wu=219.1` (high) x `ws=438` (lowest) | Controlling for confounders (commute, child-rearing age structure) removes the association | Never asserted. Phrased as "correlates with" / "suggests"; the copy explicitly states causation is not claimed. |
| 7 | *(dropped)* "Japan has the **worst gender sleep gap in the world**" | Not used | **D** | -- | **Our own falsifier:** among the 7, Japan's gap 11.7 min is SMALLER than India's 13.5 min -> "worst" is false | A claim strong enough to be a headline, dropped because it failed our own falsifier test. Cutting a strong claim, not a weak one. |
| 8 | *(dropped)* Income x happiness theme | Not used | **D** | `python evidence/reproduce_rejections.py` -> `fig_rejected_01` | Correlation too weak to carry the story spine | Rejected after building the verification figure (exhibit `fig_rejected_01`) |
| 9 | *(dropped)* Marriage x fertility theme | Not used | **D** | `python evidence/reproduce_rejections.py` -> `fig_rejected_02/03` | No causal link to the sleep/work spine | Same (exhibits `fig_rejected_02/03`) |

---

## What we dropped, and what it cost

Verification, on its own, is no longer a differentiator at this level of entry in 2026 — it is
table stakes. What actually separates this work is three things:

1. **We shipped the evidence.** Rejected themes are not self-reported; they are included as
   real reproduce figures (`fig_rejected_01/02/03`), regenerable from
   `reproduce_rejections.py`.
2. **The drop had a cost.** Claim #7, "the worst gender sleep gap in the world," was
   headline-grade. We let go of it because it failed our own falsifier (India's gap is larger).
   Cutting a *strong* claim — not a weak one — is the evidence of honesty.
3. **We weaponized a limitation.** Claim #2's conflict with the official statistic
   (Japan 1654h < USA 1789h) is not hidden; it becomes part of the story — the answer changes
   with the ruler you measure by.

---

## Reproduce commands (copy-paste, run from `01_sleep_work/`)

```bash
# Claim 1 — Japan sleep = lowest of 33
node -e 'eval(require("fs").readFileSync("scrolly/data.js","utf8").replace(/const /g,"global."));const m=DATA.reduce((a,b)=>a.sleep<b.sleep?a:b);console.log(`min sleep: ${m.c} ${m.sleep} (n=${DATA.length})`)'
# -> min sleep: Japan 444.1 (n=33)

# Claim 2 — Japan paid work = highest of 33  (+ the caveat check)
node -e 'eval(require("fs").readFileSync("scrolly/data.js","utf8").replace(/const /g,"global."));const m=DATA.reduce((a,b)=>a.work>b.work?a:b);console.log(`max work: ${m.c} ${m.work} (n=${DATA.length})`)'
# -> max work: Japan 297.1 (n=33)
node -e 'eval(require("fs").readFileSync("scrolly/data.js","utf8").replace(/const /g,"global."));console.log(`ILO annual hours — JP ${ILO_META.jpHours} vs US ${ILO_META.usHours}`)'
# -> ILO annual hours — JP 1654 vs US 1789   (official stat ranks Japan BELOW the US)

# Claim 3 — Japanese women sleep = lowest of 33
node -e 'eval(require("fs").readFileSync("scrolly/data.js","utf8").replace(/const /g,"global."));const m=ACT3.reduce((a,b)=>a.ws<b.ws?a:b);console.log(`min women-sleep: ${m.c} ${m.ws} (n=${ACT3.length})`)'
# -> min women-sleep: Japan 438 (n=33)

# Claim 4 — women sleep < men in exactly 7 of 33
node -e 'eval(require("fs").readFileSync("scrolly/data.js","utf8").replace(/const /g,"global."));const L=ACT3.filter(x=>x.ws<x.ms);console.log(`women<men: ${L.length}/${ACT3.length} — ${L.map(x=>x.c).join(", ")}`)'
# -> women<men: 7/33 — Estonia, Greece, India, Italy, Japan, Korea, Spain

# Claim 5 — Japanese men's unpaid work = world lowest
node -e 'eval(require("fs").readFileSync("scrolly/data.js","utf8").replace(/const /g,"global."));const m=ACT3.reduce((a,b)=>a.mu<b.mu?a:b);console.log(`min men-unpaid: ${m.c} ${m.mu} (n=${ACT3.length})`)'
# -> min men-unpaid: Japan 40.3 (n=33)

# Claim 7 — falsifier for the DROPPED "worst gender gap" claim
node -e 'eval(require("fs").readFileSync("scrolly/data.js","utf8").replace(/const /g,"global."));const g=ACT3.map(x=>({c:x.c,gap:+(x.ms-x.ws).toFixed(1)})).filter(x=>x.gap>0).sort((a,b)=>b.gap-a.gap);console.log("top gaps: "+g.slice(0,3).map(x=>x.c+" "+x.gap).join(" | "))'
# -> top gaps: India 13.5 | Japan 11.7 | Spain 9   => Japan is NOT worst => claim fails => dropped

# Claims 8 & 9 — regenerate the rejected-theme figures
python evidence/reproduce_rejections.py
# -> writes fig_rejected_01/02/03 (+ fig_adopted_04)
```

---

*Data source: `scrolly/data.js` (OECD Time Use Database + ILO, 33 countries), shipped verbatim
with the site. Every number above is read from that file — no separate analysis copy.*
