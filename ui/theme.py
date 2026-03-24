import streamlit as st

# Paste DARK_CSS and LIGHT_CSS here from original file
DARK_CSS = """
<style>
[data-testid="stAppViewContainer"] {
    background: radial-gradient(circle at top, #0b1220 0%, #070a12 60%, #05060b 100%);
    color: #e5e7eb;
    font-family: 'Segoe UI', sans-serif;
}
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #111827, #0b1220);
    border-right: 1px solid rgba(255,255,255,0.08);
}
[data-testid="stHeader"] { background: rgba(0,0,0,0); }
footer {visibility: hidden;}
h1, h2, h3, h4, p, label, div { color: #e5e7eb !important; }

.card {
    background: rgba(13, 17, 23, 0.55);
    border: 1px solid rgba(255,255,255,0.10);
    border-radius: 18px;
    padding: 18px;
    box-shadow: 0px 12px 28px rgba(0,0,0,0.35);
    backdrop-filter: blur(10px);
}

.signal-card {
    background: rgba(13, 17, 23, 0.75);
    border: 1px solid rgba(255,255,255,0.10);
    border-radius: 16px;
    padding: 14px 14px;
    min-height: 92px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    overflow: hidden;
}

.signal-title {
    font-size: 14px;
    font-weight: 700;
    color: #9ca3af !important;
    white-space: normal;
    word-break: break-word;
}

.signal-value {
    font-size: 16px;
    font-weight: 800;
    color: #e5e7eb !important;
    white-space: normal;
    word-break: break-word;
}

.badge-buy {
    display:inline-block;
    padding: 4px 10px;
    border-radius: 999px;
    background: rgba(34,197,94,0.18);
    border: 1px solid rgba(34,197,94,0.45);
    color: #86efac !important;
    font-weight: 800;
    font-size: 12px;
    width: fit-content;
}
.badge-sell {
    display:inline-block;
    padding: 4px 10px;
    border-radius: 999px;
    background: rgba(239,68,68,0.15);
    border: 1px solid rgba(239,68,68,0.40);
    color: #fca5a5 !important;
    font-weight: 800;
    font-size: 12px;
    width: fit-content;
}
.badge-neutral {
    display:inline-block;
    padding: 4px 10px;
    border-radius: 999px;
    background: rgba(250,204,21,0.12);
    border: 1px solid rgba(250,204,21,0.35);
    color: #fde68a !important;
    font-weight: 800;
    font-size: 12px;
    width: fit-content;
}
</style>
"""

LIGHT_CSS = """
<style>
[data-testid="stAppViewContainer"] {
    background: linear-gradient(180deg, #ffffff 0%, #f6f7fb 55%, #eef2ff 100%);
    color: #111827;
    font-family: 'Segoe UI', sans-serif;
}
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #f9fafb, #eef2ff);
    border-right: 1px solid rgba(17,24,39,0.10);
}
[data-testid="stHeader"] { background: rgba(0,0,0,0); }
footer {visibility: hidden;}
h1, h2, h3, h4, p, label, div { color: #111827 !important; }

.card {
    background: rgba(255,255,255,0.78);
    border: 1px solid rgba(17,24,39,0.10);
    border-radius: 18px;
    padding: 18px;
    box-shadow: 0px 12px 24px rgba(17,24,39,0.10);
    backdrop-filter: blur(10px);
}

.signal-card {
    background: rgba(255,255,255,0.90);
    border: 1px solid rgba(17,24,39,0.12);
    border-radius: 16px;
    padding: 14px 14px;
    min-height: 92px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    overflow: hidden;
}
.signal-title {
    font-size: 14px;
    font-weight: 700;
    color: #6b7280 !important;
    white-space: normal;
    word-break: break-word;
}
.signal-value {
    font-size: 16px;
    font-weight: 800;
    color: #111827 !important;
    white-space: normal;
    word-break: break-word;
}

.badge-buy {
    display:inline-block;
    padding: 4px 10px;
    border-radius: 999px;
    background: rgba(34,197,94,0.15);
    border: 1px solid rgba(34,197,94,0.35);
    color: #166534 !important;
    font-weight: 800;
    font-size: 12px;
    width: fit-content;
}
.badge-sell {
    display:inline-block;
    padding: 4px 10px;
    border-radius: 999px;
    background: rgba(239,68,68,0.12);
    border: 1px solid rgba(239,68,68,0.30);
    color: #991b1b !important;
    font-weight: 800;
    font-size: 12px;
    width: fit-content;
}
.badge-neutral {
    display:inline-block;
    padding: 4px 10px;
    border-radius: 999px;
    background: rgba(250,204,21,0.15);
    border: 1px solid rgba(250,204,21,0.30);
    color: #92400e !important;
    font-weight: 800;
    font-size: 12px;
    width: fit-content;
}
</style>
"""
def apply_theme(theme_name: str):
    st.markdown(DARK_CSS if theme_name == "Dark" else LIGHT_CSS, unsafe_allow_html=True)
