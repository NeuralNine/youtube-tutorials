import random
import pandas as pd

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

    # skip first 100 days to get enough data for the windows
    if context.i < 100:
        return
        
    # order target, targets the provided number of shares (so 100 = buy 100, 0 = sell 100)
    if random.random() > 0.5:
        if context.portfolio.cash >= 100 * data.current(context.asset, 'price'):
            order_target(context.asset, 100)
        else:
            print(f'Cannot buy. Insufficient funds: ${context.portfolio.cash}')
    else:
        order_target(context.asset, 0)

    record(AAPL=data.current(context.asset, 'price'))


if __name__ == "__main__":
    results = run_algorithm(
        start=pd.Timestamp("2014-01-01"),
        end=pd.Timestamp("2018-01-01"),
        initialize=initialize,
        handle_data=handle_data,
        capital_base=100000,
        data_frequency="daily",
        bundle="quandl",   # or your installed bundle
    )

    results.to_pickle("random_capped_results.pickle")
    print(results.tail())

