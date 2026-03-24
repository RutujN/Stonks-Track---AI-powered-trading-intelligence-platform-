import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# ================= SAFE IMPORTS =================
try:
    import nltk
    from nltk.sentiment.vader import SentimentIntensityAnalyzer

    try:
        nltk.data.find("sentiment/vader_lexicon.zip")
    except Exception:
        nltk.download("vader_lexicon", quiet=True)

    VADER_AVAILABLE = True
except Exception:
    VADER_AVAILABLE = False

try:
    import finnhub
    FINNHUB_AVAILABLE = True
except Exception:
    FINNHUB_AVAILABLE = False


# ================= SENTIMENT FUNCTION =================
def fetch_sentiment(symbol: str, api_key: str):
    if not (VADER_AVAILABLE and FINNHUB_AVAILABLE and api_key):
        demo = pd.DataFrame(
            {"Headline": [f"{symbol} outlook stable", "Market mixed", "Volatility watch"],
             "Score": [0.05, 0.00, -0.02]}
        )
        return float(demo["Score"].mean()), demo

    try:
        client = finnhub.Client(api_key=api_key)
        news = client.company_news(
            symbol,
            _from=(datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d"),
            to=datetime.now().strftime("%Y-%m-%d"),
        )
        headlines = [x.get("headline", "") for x in news if x.get("headline")]
        headlines = list(dict.fromkeys(headlines))[:15]

        if not headlines:
            raise ValueError("No headlines")

        sid = SentimentIntensityAnalyzer()
        scores = [sid.polarity_scores(h)["compound"] for h in headlines]

        return float(np.mean(scores)), pd.DataFrame({"Headline": headlines, "Score": scores})

    except Exception:
        demo = pd.DataFrame(
            {"Headline": [f"{symbol} outlook stable", "Market mixed", "Volatility watch"],
             "Score": [0.05, 0.00, -0.02]}
        )
        return float(demo["Score"].mean()), demo