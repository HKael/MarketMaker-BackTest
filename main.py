
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
import pandas as np

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

# Test
# data['kraken'][list(data['kraken'].keys())[2]]

# Read previously downloaded file
ob_data = pd.read_json('files/orderbooks_06jun2021.json', orient='values', typ='series')

# -- Simulation of trades (Pending)
"""
- Type A: Make a BID in Kraken, then Take BID in Bitfinex

Initialize BTC and CASH balances

Asyncronous function xemm_signal

Check Signal_BID
    Difference between BIDs on Origin and Destination is greater than Maker_Margin_BID
    Make on Destination and Take on Origin

Check Signal_ASK
    Difference between ASKs on Origin and Destination is greater than Maker_Margin_ASK
    Take on Origin and Maker on Destination

kr_maker_bid * (1 + kr_maker_fee) = bf_taker_bid * (1 - bf_taker_fee)
5942.5638 * (1 + 0.0016) = 5964.00 * (1 - 0.0020) = 0

- Type B: Take an ASK on Bitfinex, then Make an ASK in Kraken

bf_taker_bid * (1 + bf_taker_fee) = kr_maker_ask * (1 - kr_maker_fee)
6000 * (1 + 0.0020) - 6021.6346 * (1 - 0.0016) = 0
"""
