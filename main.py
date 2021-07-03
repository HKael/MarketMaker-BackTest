
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
# fees = fees_schedule(exchange='kraken', symbol=symbol, expected_volume=5)

# Massive download of OrderBook data
data = order_book(symbol=symbol, exchanges=exchanges, output='inplace', stop=None, verbose=True)
bitfinex_dates = list(data['bitfinex'].keys())
kraken_dates = list(data['kraken'].keys())

data['kraken'][kraken_dates[0]]
data['bitfinex'][bitfinex_dates[0]]
