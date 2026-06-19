import random
import pandas as pd
import talib

from zipline import run_algorithm
from zipline.api import order_target, record, symbol, set_long_only, set_max_leverage

# zipline run -f 1_random_strategy.py --start 2014-1-1 --end 2018-1-1 -o random_results.pickle --no-benchmark

def initialize(context):
    context.i = 0  # start at day 0
    context.asset = symbol('AAPL')

    set_long_only()
    set_max_leverage(1.0)


def handle_data(context, data):
    context.i += 1  # move one day forward

    # skip first 50 days to get enough data for the windows
    if context.i < 50:
        return

    prices = data.history(context.asset, 'price', bar_count=50, frequency='1d')

    macd, signal, hist = talib.MACD(
        prices,
        fastperiod=12,
        slowperiod=26,
        signalperiod=9
    )

    macd = macd[-1]
    signal = signal[-1]
    hist = hist[-1]

    price = data.current(context.asset, 'price')

    # order target, targets the provided number of shares (so 100 = buy 100, 0 = sell 100)
    if macd > signal:
        if context.portfolio.cash >= 100 * price:
            order_target(context.asset, 100)
    elif macd < signal:
        order_target(context.asset, 0)

    record(AAPL=price, macd=macd, signal=signal, hist=hist)





if __name__ == "__main__":
    results = run_algorithm(
        start=pd.Timestamp("2014-01-01"),
        end=pd.Timestamp("2026-01-01"),
        initialize=initialize,
        handle_data=handle_data,
        capital_base=10000,
        data_frequency="daily",
        bundle="yfinance-csvdir-bundle",   # or your installed bundle
    )

    results.to_pickle("macd_yfinance_results.pickle")
    print(results.tail())
