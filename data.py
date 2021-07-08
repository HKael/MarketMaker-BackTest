
# -- --------------------------------------------------------------------------------------------------- -- #
# -- MarketMaker-BackTest                                                                                -- #
# -- --------------------------------------------------------------------------------------------------- -- #
# -- file: data.py                                                                                       -- #
# -- Description: Data sources and processing                                                            -- #
# -- --------------------------------------------------------------------------------------------------- -- #
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

# --------------------------------------------------------------------------- EXCHANGE TRANSACTIONS FEEs -- # 
# --------------------------------------------------------------------------------------------------------- #

def fees_schedule(exchange, symbol, expected_volume):
    """
    To get the fee schedule of an already initialized client-exchange, including the case where there is
    a tierBased list provided by ccxt library.

    Parameters
    ----------
    
    exchange: str
        with exchange to be connected to
    
    expected_volume: numeric
        With a montly expected volume of transactions, expressed in USD. 

    Returns
    -------

    r_exchange_fees: dict
        with 'taker' and 'maker' fees expressed in basis points.

    References
    ----------

        All the information currently available is obtained from ccxt already integrated API to differen
        exchanges, which according to [1] it support more than 120 bitcoin/altcoin exchanges. In order to
        validate fee schedule of initialized client-exchange, please refer to the documentation of that
        particular exchange. The example include reference url for two exchanges: Bitfinex [2] and Kraken [3].

        [1] https://github.com/ccxt/ccxt
        [2] https://www.bitfinex.com/fees/
        [3] https://www.kraken.com/en-us/features/fee-schedule

    """

    # Initialize client
    client_exchange = getattr(ccxt, exchange)({'enableRateLimit': True})
    client_markets = client_exchange.load_markets()

    # In case ccxt has registered a tierBased list of fees
    if client_markets[symbol]['tierBased']:
        try:
            # locate the clossest tier value according to a given monthly expected volume (provided in USD)
            idx = np.array([abs(i[0] - expected_volume)
                            for i in client_markets[symbol]['tiers']['taker']]).argmin()
            r_exchange_fees = {'taker': client_markets[symbol]['tiers']['taker'][idx][1],
                               'maker': client_markets[symbol]['tiers']['maker'][idx][1]}
        except:
            print('Tier was not found, returning the highest fee value')
            # In case of exception in the tier search, return the values of the first position
            r_exchange_fees = {'taker': client_markets[symbol]['tiers']['taker'][0][1],
                               'maker': client_markets[symbol]['tiers']['maker'][0][1]}
            
    else:
        # In case a tierBased fee schedule is not supported, the standard value returned from ccxt is used.
        r_exchange_fees = {'taker': client_markets[symbol]['taker'],
                           'maker': client_markets[symbol]['maker']}
    
    # Return final data
    return r_exchange_fees

# --------------------------------------------------------------------------- ASYNCRONOUS ORDERBOOK DATA -- # 
# --------------------------------------------------------------------------------------------------------- #

def order_book(symbol, exchanges, execution='async', stop=None, output=None, verbose=True):
    """
    Asyncronous OrderBook data fetcher. It will asyncronously catch innovations of transactions whenever they
    occur for every exchange is included in the list exchanges, and return the complete orederbook in a in a
    JSON format or DataFrame format with 'ask', 'ask_size', 'bid', 'bid_size'.

    Parameters
    ----------

    symbol: list
        with the names of instruments or markets to fetch the oredebook from.

    exchanges: list
        with the names of exchanges from where the data is intended to be fetched.
    
    execution: str
        'async': Asyncronous option to fetch several orderbooks in the same call. Depends on 
                 asyncio and ccxt.async_support
        'parallel': Run a parallel processing to deploy 1 instance for each symbol at each market. Depends
                 on multiprocessing (pending)

    stop: dict
        Criteria to stop the execution. Default behavior will be to stop after 1 minute of running.

        'min_count': int 
            Stops when all orderbooks have, at least, this number of registred timestamps.
        'target_timestamp': datetime
            Stops when its reached a specific timestamp.
        None: (default)
            Stop when 1 minute has elapsed

    output: str
        Options for the output. Default is inplace
        'JSON': will write a JSON file (pending)
        'inplace': Delivers the result in a pd.DataFrame inplace
    
    verbose: bool
        To print in real time the fetched first ask and bid of every exchange.

    Returns
    -------

    r_data: dict
        A dictionary with the fetched data, with the following structure.

        r_data = {
            instrument: {
                exchange: {
                    
                    timestamp: {'ask': 1.4321, 'ask_size': 0.12,
                                'bid': 1.1234, 'bid_size': 0.21},
                    
                    timestamp: {'ask': 1.4321, 'ask_size': 0.12,
                                'bid': 1.1234, 'bid_size': 0.21}
            }
        }

    References
    ----------

    [1] https://github.com/ccxt/ccxt
    [2] https://docs.python.org/3/library/asyncio.html

    """
    
    # Store data for every exchange in the list
    r_data = {'bitfinex': {}, 'kraken': {}}

    # ----------------------------------------------------------------------------- ASYNCRONOUS REQUESTS -- # 
    async def async_client(exchange, symbol):

        # Await to be inside exchange limits of calls
        # await asyncio.sleep(exchange.rateLimit / 1000)

        # Initialize client inside the function, later will be closed, since this is runned asyncronuously
        # more than 1 client could be created and later closed.
        client = getattr(ccxt_async, exchange)({'enableRateLimit': True})
        await client.load_markets()

        # Check for symbol support on exchange
        if symbol not in client.symbols:
            raise Exception(exchange + ' does not support symbol ' + symbol)   

        # Initial time and counter
        time_1 = time.time()
        time_f = 0

        # Loop until stop criteria is reached
        while time_f <= 60:
            
            # Try and await for client response
            try:

                # Fetch, await and get datetime
                orderbook = await client.fetch_order_book(symbol)
                datetime = client.iso8601(client.milliseconds())

                # Verbosity
                if verbose:
                    print(datetime, client.id, symbol, orderbook['bids'][0], orderbook['asks'][0])

                # Unpack values
                ask_price, ask_size = np.array(list(zip(*orderbook['asks']))[0:2])
                bid_price, bid_size = np.array(list(zip(*orderbook['bids']))[0:2])
                spread = np.round(ask_price - bid_price, 4)
               
                # Final data format for the results
                r_data[client.id].update({datetime: pd.DataFrame({'ask_size': ask_size, 'ask': ask_price,
                                                                  'bid': bid_price, 'bid_size': bid_size,
                                                                  'spread': spread}) })
                # End time
                time_2 = time.time()
                time_f = round(time_2 - time_1, 4)

            # In case something bad happens with client
            except Exception as e:
                print(type(e).__name__, e.args, str(e))
                pass

        # Close client
        await client.close()

    # ------------------------------------------------------------------------------ MULTIPLE ORDERBOOKS -- # 
    async def multi_orderbooks(exchanges, symbol):
        # A list of routines (and parameters) to run
        input_coroutines = [async_client(exchange, symbol) for exchange in exchanges]
        # wait for responses
        await asyncio.gather(*input_coroutines, return_exceptions=True)

    # Run event loop in async
    if execution=='async':
        asyncio.get_event_loop().run_until_complete(multi_orderbooks(exchanges, symbol))

    # Run multiple events in parallel
    elif execution=='parallel':
        raise ValueError('Only supported async')
    
    # Raise error in case of other value
    else:
        raise ValueError(execution, 'is not supported as a type of execution')

    # ----------------------------------------------------------------------------------- TYPE OF OUTPUT -- #

    # A JSON file writen in directory
    if output == 'JSON':
        # Serializing json 
        json_object = pd.DataFrame(r_data).to_json()
        
        # Writing to sample.json
        with open("files/orderbooks_06jun2021.json", "w") as outfile:
            outfile.write(json_object)

    # Just return the DataFrame
    elif output == 'inplace':
        return r_data
    
    # Invalid output
    else:
        raise ValueError('Invalid output value')

# ---------------------------------------------------------------------------- CONTINUOUS ORDERBOOK DATA -- # 
# --------------------------------------------------------------------------------------------------------- #

def continuous_ob(orderbooks):
    """
    Creates a continuous orderbook timeseries data, for all orderbooks included as input. i.e. all timestamps
    that one orderbook has and the other dont, in the latter repeates the information of the former, with
    this, the output will deliver two historical orderbooks with the same timestamp.

    Parameters
    ----------
    orderbooks: dict
        With 2 or more orderbooks data. 

    Returns
    -------
    r_ts_orderbooks: dict
        With the 2 or more orderbooks now all of them with the same timestamps

    """
    # orderbooks = ob_data.copy()
    exchanges = list(orderbooks.keys())
    
    timestamps = []
    # Create a joined list of all the dates among all the exchanges
    # [timestamps.append(orderbooks[exchanges[0]].keys()) for exchange in exchanges]

    # If for an exchange the timestamp does not contain info, use the previous timestamp that does
   
    return 1
