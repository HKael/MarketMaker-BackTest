
# -- --------------------------------------------------------------------------------------------------- -- #
# -- MarketMaker-BackTest                                                                                -- #
# -- --------------------------------------------------------------------------------------------------- -- #
# -- Description: Code for a proof of concept of a market-maker backtest                                 -- #
# -- Author: IFFranciscoME - if.francisco.me@gmail.com                                                   -- #
# -- license: MIT License                                                                                -- #
# -- Repository: https://github.com/IFFranciscoME/MarketMaker-BackTest                                   -- #
# --------------------------------------------------------------------------------------------------------- #

# -- Load packages
import numpy as np
import ccxt

# Symbol
symbol = 'BTC/EUR'
exchanges = ["bitfinex", "kraken"]
exchange_id = exchanges[0]

# Expected Volume (In case of tierBased fees)
expected_volume = 0

# Exchange class
exchange = getattr(ccxt, exchange_id)({'enableRateLimit': True})
markets = exchange.load_markets()

# -- Get transaction fees  -- # 
if markets[symbol]['tierBased']:
    try:
        idx = np.array([abs(i[0] - expected_volume) for i in markets[symbol]['tiers']['taker']]).argmin()
        fees = {'taker': markets[symbol]['tiers']['taker'][idx][1],
                'maker': markets[symbol]['tiers']['maker'][idx][1]}
    except:
        print('Tier was not found, returning the highest fee value')
    finally:
        fees = {'taker': markets[symbol]['tiers']['taker'][0][1],
                'maker': markets[symbol]['tiers']['maker'][0][1]}
else:         
    fees = {'taker': markets[symbol]['taker'], 'maker': markets[symbol]['maker']}
