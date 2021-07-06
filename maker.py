
# -- --------------------------------------------------------------------------------------------------- -- #
# -- MarketMaker-BackTest                                                                                -- #
# -- --------------------------------------------------------------------------------------------------- -- #
# -- Description: Code for a proof of concept of a market-maker backtest                                 -- #
# -- Author: IFFranciscoME - if.francisco.me@gmail.com                                                   -- #
# -- license: MIT License                                                                                -- #
# -- Repository: https://github.com/IFFranciscoME/MarketMaker-BackTest                                   -- #
# --------------------------------------------------------------------------------------------------------- #

# -- Load base packages
import pandas as pd
import numpy as np
import time
import json

# -- Cryptocurrency data and trading API
import ccxt

# -- Asyncronous data fetch
import asyncio
import ccxt.async_support as ccxt_async

# ----------------------------------------------------------------------------------------- SIGNAL MAKER -- # 
# --------------------------------------------------------------------------------------------------------- #

def xemm_signal(prices, fees):
    """
    Signal generation to bakctest a Cross-Exchange Market Maker strategy.

    Parameters
    ----------

    prices: dict
        with the historical ticks or prices, must be a dictionary with the following structure:
            {'origin_exchange: {timestamp: {}}, 'destination_exchange': {}}

    fees: dict
        with the fee schedule for each exchange

    

    Returns
    -------

    References
    ----------

    """

    # Optional, to drop keys with no values (when dict stores all dates for both exchanges)
    # ob_data['kraken'] = {k: v for k, v in ob_data['kraken'].items() if v is not None}
    # ob_data['bitfinex'] = {k: v for k, v in ob_data['bitfinex'].items() if v is not None}

    # dates
    # bitfinex_dates = list(ob_data['bitfinex'].keys())
    # kraken_dates = list(ob_data['kraken'].keys())

    return 1
