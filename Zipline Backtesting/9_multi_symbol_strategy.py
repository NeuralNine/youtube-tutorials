import random
import pandas as pd
import talib

from zipline import run_algorithm
from zipline.api import order_target_percent, record, symbol, set_long_only, set_max_leverage

# zipline run -f 1_random_strategy.py --start 2014-1-1 --end 2018-1-1 -o random_results.pickle --no-benchmark

def initialize(context):
    context.i = 0  # start at day 0
    context.assets = [
        symbol('AAPL'),
        symbol('META'),
        symbol('GOOG'),
        symbol('NVDA'),
        symbol('TSLA'),
    ]

    context.target_weight = 0.19

    set_long_only()
    set_max_leverage(1.0)


def handle_data(context, data):
    context.i += 1  # move one day forward

    # skip first 50 days to get enough data for the windows
    if context.i < 50:
        return

    for asset in context.assets:
        if not data.can_trade(asset):
            continue

        prices = data.history(asset, 'price', bar_count=50, frequency='1d')

        macd, signal, hist = talib.MACD(
            prices,
            fastperiod=12,
            slowperiod=26,
            signalperiod=9
        )

        macd = macd[-1]
        signal = signal[-1]
        hist = hist[-1]

        price = data.current(asset, 'price')

        # order target percent, targets portfolio weight, so 0.19 = 19%, 0.0 = sell/close
        if macd > signal:
            order_target_percent(asset, context.target_weight)
        elif macd < signal:
            order_target_percent(asset, 0.0)

        record(
            **{
                f'{asset.symbol}_price': price,
                f'{asset.symbol}_macd': macd,
                f'{asset.symbol}_signal': signal,
                f'{asset.symbol}_hist': hist,
            }
        )





if __name__ == "__main__":
    results = run_algorithm(
        start=pd.Timestamp("2014-01-02"),
        end=pd.Timestamp("2025-12-31"),
        initialize=initialize,
        handle_data=handle_data,
        capital_base=10000,
        data_frequency="daily",
        bundle="yfinance-csvdir-bundle",   # or your installed bundle
    )

    results.to_pickle("multi_stock_macd_yfinance_results.pickle")
    print(results.tail())
