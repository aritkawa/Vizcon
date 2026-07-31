r"""
VizCon 2026 - Streamlit ホスティング版
本体HTML(index_ja.html / index.html)を単一ソースとして配信する薄いラッパー。
- 本体は外部 data.js を参照するが iframe(srcdoc)内では相対参照が切れるため、
  配信時に data.js を <script> にインライン展開する。
- 言語切替は画面上部の常時表示トグルで行う(Streamlitネイティブ。確実に動く)。
  本体ページ内の右上リンクは iframe サンドボックスがトップ遷移を遮断し機能しないため配信時に除去。
　実行用コマンド：.venv\Scripts\streamlit run app.py
"""
import os
import base64
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="The World's Most Diligent Insomniacs",
    page_icon="🌙",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown(
    """
    <style>
      #MainMenu, header, footer {visibility: hidden;}
      .stApp {background: #0f1220;}
      .block-container {padding: .5rem 1rem 0 !important; max-width: 100% !important;}
      div[data-testid="stHorizontalBlock"] {align-items: center;}
      iframe {border: none;}
      /* 言語トグルの文字を見やすく(ダーク背景対策) */
      div[data-testid="stRadio"] label p {
        color: #f3f1e9 !important;
        font-size: 17px !important;
        font-weight: 700 !important;
        letter-spacing: .02em;
      }
      div[data-testid="stRadio"] div[role="radiogroup"] { gap: 1.4rem; }
      /* ラジオの丸をアンバー(選択色)で強調 */
      div[data-testid="stRadio"] [data-baseweb="radio"] div:first-child {
        border-color: #c9973f !important;
      }
    </style>
    """,
    unsafe_allow_html=True,
)

BASE = os.path.dirname(os.path.abspath(__file__))
SCROLLY = os.path.join(BASE, "scrolly")
HTML_FILES = {"日本語": "index_ja.html", "English": "index.html"}


def load_html(fname):
    with open(os.path.join(SCROLLY, fname), "r", encoding="utf-8") as f:
        html = f.read()
    with open(os.path.join(SCROLLY, "data.js"), "r", encoding="utf-8") as f:
        data_js = f.read()
    html = html.replace(
        '<script src="data.js"></script>', f"<script>\n{data_js}\n</script>"
    )
    # iframe内で機能しない言語リンクを除去(切替は上部トグルへ一本化)
    for nav in (
        '<nav class="lang"><a href="index.html">EN</a></nav>',
        '<nav class="lang"><a href="index_ja.html">日本語</a></nav>',
    ):
        html = html.replace(nav, "")
    # 背景動画: iframe(srcdoc)内は相対参照が切れるため data URI でインライン展開
    vid = os.path.join(SCROLLY, "assets", "hero_sky.webm")
    if os.path.exists(vid):
        with open(vid, "rb") as f:
            b64 = base64.b64encode(f.read()).decode("ascii")
        html = html.replace(
            '<source src="assets/hero_sky.webm" type="video/webm">',
            f'<source src="data:video/webm;base64,{b64}" type="video/webm">',
        )
    return html


# --- 上部: 言語トグル(常時表示) ---
lang = st.radio(
    "言語 / Language",
    list(HTML_FILES.keys()),
    horizontal=True,
    label_visibility="collapsed",
)

components.html(load_html(HTML_FILES[lang]), height=1000, scrolling=True)
