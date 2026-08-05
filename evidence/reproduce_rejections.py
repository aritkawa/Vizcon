# -*- coding: utf-8 -*-
"""
VizCon 2026 "The World's Most Diligent Insomniacs"
GenAI活用ドキュメント 証拠物件: テーマ検証(棄却/採用)の散布図を再現する。

元の検証は 2026-07-08〜09 および 07-12 に Aki(AI)との対話セッションで実施。
本スクリプトは当時と同じ生データ(C:/Viz 配下)から同じ結論を再現する。
実行: streamlit_app/.venv の python で python reproduce_rejections.py
出力: evidence/fig_*.png 4枚 + コンソールに相関値
"""
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

plt.rcParams["font.family"] = "Meiryo"
plt.rcParams["figure.dpi"] = 150

BASE = "C:/Viz"
OUT = f"{BASE}/01_sleep_work/evidence"

INK = "#1b2440"; AMBER = "#c8922a"; RED = "#c0392b"; GREY = "#8a90a2"

def style(ax, title, sub):
    ax.set_title(title, fontsize=12, fontweight="bold", color=INK, loc="left", pad=42)
    ax.text(0, 1.025, sub, transform=ax.transAxes, fontsize=8.5, color=GREY, va="bottom")
    for s in ["top", "right"]:
        ax.spines[s].set_visible(False)
    ax.grid(alpha=0.25, linewidth=0.5)

def corr(a, b):
    m = a.notna() & b.notna()
    return float(np.corrcoef(a[m], b[m])[0, 1]), int(m.sum())

# ---------------------------------------------------------------
# 図1【棄却】所得×幸福 — 相関が強すぎて発見(Discovery)がない
# ---------------------------------------------------------------
gdp = pd.read_csv(f"{BASE}/02_money_happiness/gdp_per_capita_worldbank.csv")
hap = pd.read_csv(f"{BASE}/02_money_happiness/happiness_cantril_ladder.csv")
gdp.columns = ["Entity", "Code", "Year", "gdp", "region"]
hap.columns = ["Entity", "Code", "Year", "life_sat"]
yr = int(min(gdp.Year.max(), hap.Year.max()))
m1 = pd.merge(gdp[gdp.Year == yr], hap[hap.Year == yr], on=["Entity", "Code"])
m1 = m1[m1.Code.notna() & (m1.Code != "OWID_WRL")]
m1["log_gdp"] = np.log10(m1.gdp)
r1, n1 = corr(m1.log_gdp, m1.life_sat)

fig, ax = plt.subplots(figsize=(7, 5))
ax.scatter(m1.gdp, m1.life_sat, s=18, color=INK, alpha=0.55)
jp = m1[m1.Code == "JPN"]
if len(jp):
    ax.scatter(jp.gdp, jp.life_sat, s=60, color=RED, zorder=5)
    ax.annotate("日本", (jp.gdp.iloc[0], jp.life_sat.iloc[0]),
                xytext=(8, -16), textcoords="offset points", color=RED, fontsize=9)
ax.set_xscale("log")
ax.set_xlabel("一人あたりGDP (log, int-$)", fontsize=9)
ax.set_ylabel("生活満足度 (Cantril ladder)", fontsize=9)
style(ax, f"【棄却】所得 × 幸福度  r = {r1:.3f} (log所得, N={n1}, {yr}年)",
      "強すぎる相関 = 誰も驚かない。「天井(サチュレーション)」も出ず、\nDiscoveryが無いためテーマ棄却 (2026-07-08)")
fig.tight_layout(); fig.savefig(f"{OUT}/fig_rejected_01_money_happiness.png"); plt.close(fig)
print(f"[1] 所得×幸福: r={r1:.3f} N={n1} ({yr})")

# ---------------------------------------------------------------
# 図2【棄却】結婚×少子化 — 全世界では相関ほぼゼロ、条件付きでしか語れない
# ---------------------------------------------------------------
bom = pd.read_csv(f"{BASE}/03_marriage_fertility/births_outside_marriage.csv")
tfr = pd.read_csv(f"{BASE}/03_marriage_fertility/total_fertility_rate.csv")
bom.columns = ["Entity", "Code", "Year", "bom"]
tfr.columns = ["Entity", "Code", "Year", "tfr"]
# 各国の婚外子率 最新年 に同年TFRを結合
bom_latest = bom.sort_values("Year").groupby("Code", as_index=False).last()
m2 = pd.merge(bom_latest, tfr, on=["Code", "Year"], suffixes=("", "_t"))
m2 = m2[m2.Code.str.len() == 3]
r2_all, n2_all = corr(m2.bom, m2.tfr)
# 欧州+東アジア サブセット(当時の検証と同じ趣旨: 出生登録文化が異なる地域を除外)
# 注: 当時のスパイク値(全世界0.029/サブセット0.574, 41/32カ国)とは国リストと年マッチの
#     細部が異なるため数値は完全一致しないが、「全世界では消え、サブセットでのみ
#     中程度の相関が浮く=条件付きでしか語れない」という棄却根拠の構造は同一。
EU_EA = {"AUT", "BEL", "BGR", "HRV", "CYP", "CZE", "DNK", "EST", "FIN", "FRA", "DEU",
         "GRC", "HUN", "ISL", "IRL", "ITA", "LVA", "LTU", "LUX", "MLT", "NLD", "NOR",
         "POL", "PRT", "ROU", "SVK", "SVN", "ESP", "SWE", "CHE", "GBR", "TUR",
         "JPN", "KOR"}
m2e = m2[m2.Code.isin(EU_EA)]
r2_sub, n2_sub = corr(m2e.bom, m2e.tfr)

fig, ax = plt.subplots(figsize=(7, 5))
ax.scatter(m2.bom, m2.tfr, s=18, color=GREY, alpha=0.5, label=f"全世界 r={r2_all:.3f} (N={n2_all})")
ax.scatter(m2e.bom, m2e.tfr, s=22, color=INK, alpha=0.75, label=f"欧州+東アジア r={r2_sub:.3f} (N={n2_sub})")
for code, name in [("JPN", "日本"), ("KOR", "韓国"), ("FRA", "フランス")]:
    row = m2[m2.Code == code]
    if len(row):
        ax.scatter(row.bom, row.tfr, s=60, color=RED, zorder=5)
        ax.annotate(name, (row.bom.iloc[0], row.tfr.iloc[0]),
                    xytext=(6, 6), textcoords="offset points", color=RED, fontsize=9)
ax.set_xlabel("婚外子率 (%)", fontsize=9)
ax.set_ylabel("合計特殊出生率 (TFR)", fontsize=9)
ax.legend(fontsize=8, frameon=False)
style(ax, "【棄却】結婚 × 少子化 — 全世界では相関が消える",
      "サブセット限定でしか語れない条件付き相関\n+ 地雷3つ(COVID年の誇張/出生登録文化差/既知感) → 棄却 (2026-07-09)")
fig.tight_layout(); fig.savefig(f"{OUT}/fig_rejected_02_marriage_fertility.png"); plt.close(fig)
print(f"[2] 結婚×少子化: 全世界 r={r2_all:.3f} N={n2_all} / サブセット r={r2_sub:.3f} N={n2_sub}")

# ---------------------------------------------------------------
# 図3【棄却】幸福度×無償労働男女差 — 再スパイクで減衰した拡張案
# ---------------------------------------------------------------
summ = pd.read_csv(f"{BASE}/01_sleep_work/QS_ready/qs_country_summary.csv", encoding="utf-8-sig")
summ["yr"] = summ["survey_year"].astype(str).str.extract(r"(\d{4})").astype(float)
def match_hap(country, yr_):
    sub = hap[hap.Entity == country]
    if sub.empty:
        sub = hap[hap.Entity == {"Korea": "South Korea"}.get(country, "")]
    if sub.empty or pd.isna(yr_):
        return np.nan
    return sub.loc[(sub.Year - yr_).abs().idxmin(), "life_sat"]
summ["life_sat"] = [match_hap(c, y) for c, y in zip(summ.country, summ.yr)]
r3, n3 = corr(summ.life_sat, summ.unpaid_gap_women_minus_men)

fig, ax = plt.subplots(figsize=(7, 5))
ax.scatter(summ.unpaid_gap_women_minus_men, summ.life_sat, s=26, color=INK, alpha=0.7)
jp = summ[summ.is_japan == 1]
ax.scatter(jp.unpaid_gap_women_minus_men, jp.life_sat, s=70, color=RED, zorder=5)
ax.annotate("日本", (jp.unpaid_gap_women_minus_men.iloc[0], jp.life_sat.iloc[0]),
            xytext=(8, -4), textcoords="offset points", color=RED, fontsize=9)
ax.set_xlabel("無償労働の男女差 (女性-男性, 分/日)", fontsize=9)
ax.set_ylabel("生活満足度 (Cantril ladder)", fontsize=9)
style(ax, f"【棄却】幸福度 × 無償労働男女差  r = {r3:.3f} (N={n3})",
      "初回スパイク r=-0.74 → 調査年マッチを厳密化した再スパイクで減衰\n→ 幕として弱く不採用 (2026-07-16)")
fig.tight_layout(); fig.savefig(f"{OUT}/fig_rejected_03_happiness_unpaidgap.png"); plt.close(fig)
print(f"[3] 幸福×無償労働差: r={r3:.3f} N={n3}")

# ---------------------------------------------------------------
# 図4【採用】労働ランク×睡眠ランクの「ねじれ」 — 作品の柱
# ---------------------------------------------------------------
fig, ax = plt.subplots(figsize=(7, 5))
ax.scatter(summ.pure_work_min, summ.sleep_min, s=26, color=INK, alpha=0.7)
r4, n4 = corr(summ.pure_work_min, summ.sleep_min)
jp = summ[summ.is_japan == 1]
ax.scatter(jp.pure_work_min, jp.sleep_min, s=90, color=RED, zorder=5)
ax.annotate("日本\n労働1位・睡眠33位", (jp.pure_work_min.iloc[0], jp.sleep_min.iloc[0]),
            xytext=(-130, 6), textcoords="offset points", color=RED, fontsize=9, fontweight="bold")
ax.set_xlabel("純粋労働時間 (分/日)", fontsize=9)
ax.set_ylabel("睡眠時間 (分/日)", fontsize=9)
style(ax, f"【採用】労働 × 睡眠  r = {r4:.3f} (OECD TUS 33カ国)",
      "外れ値としての日本=「世界一働き、世界一寝ていない」。\n棄却2案と違い、1点の異常が物語になる → 採用 (2026-07-09)")
fig.tight_layout(); fig.savefig(f"{OUT}/fig_adopted_04_work_sleep.png"); plt.close(fig)
print(f"[4] 労働×睡眠(採用): r={r4:.3f} N={n4} / 日本 work={jp.pure_work_min.iloc[0]} sleep={jp.sleep_min.iloc[0]}")
print("done ->", OUT)
