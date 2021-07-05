
# -- --------------------------------------------------------------------------------------------------- -- #
# -- MarketMaker-BackTest                                                                                -- #
# -- --------------------------------------------------------------------------------------------------- -- #
# -- Description: Code for a proof of concept of a market-maker backtest                                 -- #
# -- Author: IFFranciscoME - if.francisco.me@gmail.com                                                   -- #
# -- license: MIT License                                                                                -- #
# -- Repository: https://github.com/IFFranciscoME/MarketMaker-BackTest                                   -- #
# --------------------------------------------------------------------------------------------------------- #

# -- Load Packages for this script
import pandas as pd
import json

# -- Load base packages
from data import fees_schedule, order_book

# Small test
exchanges = ["bitfinex", "kraken"]
symbol = 'BTC/EUR'
expected_volume = 0

# Get fee schedule
# fees = fees_schedule(exchange='kraken', symbol=symbol, expected_volume=expected_volume)

# Massive download of OrderBook data
# data = order_book(symbol=symbol, exchanges=exchanges, output='inplace', stop=None, verbose=True)

# Read previously downloaded file
data = pd.read_json('files/orderbooks_05jul21.json', orient='values', typ='series')
# Optional, to drop keys with no values (when dict stores all dates for both exchanges)
data['kraken'] = {k: v for k, v in data['kraken'].items() if v is not None}
data['bitfinex'] = {k: v for k, v in data['bitfinex'].items() if v is not None}

# dates
bitfinex_dates = list(data['bitfinex'].keys())
kraken_dates = list(data['kraken'].keys())
r_spread = {exchange:[] for exchange in exchanges}

# Spread Historical TimeSeries Data
for exchange in exchanges:
    print(exchange)
    for k_i in list(data[exchange].keys()):
        # exchange = exchanges[1]
        # k_i = list(data[exchange].keys())[0]

        top_ob = pd.DataFrame(data[exchange][k_i]).iloc[0]
        # print(top_ob)
        spread = top_ob['ask'] - top_ob['bid']
        # print(spread)
        r_spread[exchange].append(spread)
