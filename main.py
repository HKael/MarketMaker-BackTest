
# -- --------------------------------------------------------------------------------------------------- -- #
# -- MarketMaker-BackTest                                                                                -- #
# -- --------------------------------------------------------------------------------------------------- -- #
# -- Description: Code for a proof of concept of a market-maker backtest                                 -- #
# -- Author: IFFranciscoME - if.francisco.me@gmail.com                                                   -- #
# -- license: MIT License                                                                                -- #
# -- Repository: https://github.com/IFFranciscoME/MarketMaker-BackTest                                   -- #
# --------------------------------------------------------------------------------------------------------- #

# -- Load base packages
from data import fees_schedule, order_book

# Small test
exchanges = ["bitfinex", "kraken"]
symbol = 'BTC/EUR'
expected_volume = 0

# Get fee schedule
fees = fees_schedule(exchange='kraken', symbol=symbol, expected_volume=5)

# Massive download of OrderBook data
data = order_book(symbol=symbol, exchanges=exchanges, stop=None, verbose=True)
data['bitfinex'][list(data['bitfinex'].keys())[0]].head()
