import streamlit as st

# Paste badge_class and render_signal_cards here
def badge_class(action: str) -> str:
    if action == "BUY":
        return "badge-buy"
    if action == "SELL":
        return "badge-sell"
    return "badge-neutral"


def render_signal_cards(sigs):
    if not sigs:
        st.warning("Not enough data to generate signals.")
        return

    cols = st.columns(min(5, len(sigs)))
    for i, (title, value, action) in enumerate(sigs):
        with cols[i % len(cols)]:
            st.markdown(
                f"""
                <div class="signal-card">
                    <div class="signal-title">{title}</div>
                    <div class="signal-value">{value}</div>
                    <div class="{badge_class(action)}">{action}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )