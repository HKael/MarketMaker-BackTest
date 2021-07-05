
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

# -- Load base packages
from data import fees_schedule, order_book

# Small test
exchanges = ["bitfinex", "kraken"]
symbol = 'BTC/EUR'
expected_volume = 0

# Get fee schedule
fees = fees_schedule(exchange='kraken', symbol=symbol, expected_volume=expected_volume)

# Massive download of OrderBook data
# data = order_book(symbol=symbol, exchanges=exchanges, output='inplace', stop=None, verbose=True)

# Read previously downloaded file
ob_data = pd.read_json('files/orderbooks_05jul21.json', orient='values', typ='series')

# Optional, to drop keys with no values (when dict stores all dates for both exchanges)
ob_data['kraken'] = {k: v for k, v in ob_data['kraken'].items() if v is not None}
ob_data['bitfinex'] = {k: v for k, v in ob_data['bitfinex'].items() if v is not None}

# dates
bitfinex_dates = list(ob_data['bitfinex'].keys())
kraken_dates = list(ob_data['kraken'].keys())
r_spread = {exchange:[] for exchange in exchanges}

# Spread Historical TimeSeries Data
for exchange in exchanges:
    for k_i in list(ob_data[exchange].keys()):
        top_ob = pd.DataFrame(ob_data[exchange][k_i]).iloc[0]
        spread = top_ob['ask'] - top_ob['bid']
        r_spread[exchange].append(spread)

# -- Simulation of trades (Pending)
"""
- Type A: Make a BID in Kraken, then Take BID in Bitfinex

kr_maker_bid * (1 + kr_maker_fee) = bf_taker_bid * (1 - bf_taker_fee)
5942.5638 * (1 + 0.0016) = 5964.00 * (1 - 0.0020) = 0

- Type B: Take an ASK on Bitfinex, then Make an ASK in Kraken

bf_taker_bid * (1 + bf_taker_fee) = kr_maker_ask * (1 - kr_maker_fee)
6000 * (1 + 0.0020) - 6021.6346 * (1 - 0.0016) = 0
"""
