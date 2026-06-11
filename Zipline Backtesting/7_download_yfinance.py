import pandas as pd
import yfinance as yf

tickers = ["AAPL", "META", "GOOG", "NVDA", "TSLA"]

for ticker in tickers:
    df = yf.Ticker(ticker).history(
        start="2014-01-02",
        end="2026-01-02",
        auto_adjust=True,
        actions=False
    )

    df = df.reset_index()

    df = df.rename(columns={
        "Date": "date",
        "Open": "open",
        "High": "high",
        "Low": "low",
        "Close": "close",
        "Volume": "volume"
    })

    df["date"] = pd.to_datetime(df["date"]).dt.strftime("%Y-%m-%d")

    df["dividend"] = 0.0
    df["split"] = 1.0

    df = df[[
        "date",
        "open",
        "high",
        "low",
        "close",
        "volume",
        "dividend",
        "split"
    ]]

    for column in ["open", "high", "low", "close", "volume", "dividend", "split"]:
        df[column] = pd.to_numeric(df[column])

    df = df.dropna()

    df.to_csv(f"./zipline_csvs/daily/{ticker}.csv", index=False)
