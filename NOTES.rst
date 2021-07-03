
====================
NOTES & CALCULATIONS
====================

# -- Arbitrage version (Less cost efficient) -------------------------------------------------------------- # 
# --------------------------------------------------------------------------------------------------------- # 

On Origin, Take an existing ASK to BUY 1 BTC, on Destination, take an existing BID to SELL 1 BTC

Buy : Take 1 BTC @6000 ASK on Bitfinex
Sell: Take 1 BTC @ BID on Kraken

# Bitfinex (Taker to the ASK)
taker_price_ask * (1 - taker_fee) = 6000.000 * (1 - 0.0020) = 5988.00
# Kraken (Taker from the BID)
taker_price_bid * (1 - taker_fee) = taker_price_bid * (1 - 0.0026)

# Formula
5988.00 - taker_price_bid * (1 - 0.0026) = 0
taker_price_bid = + 5988.00 / (1 - 0.0026)

taker_price_bid = 6003.609384399
spread = 6021.63 - 6003.609384399 = 18.0206 Eur or 29.92 Bp from ASK in Kraken

# -- Bitfinex
ASK = 6000.00 EUR
BID = 5964.00 EUR
Spread = 6000.00 - 5964.00 = 36 EUR or 60 bp

# -- Kraken
ASK = 6021.63 EUR
BID = 6003.6094 EUR
Spread = 6021.63 EUR - 6003.6094 EUR = 18.0206 EUR or 29.9264 bp

# -- Numerical Proof
bf_taker_ask * (1 - taker_fee) = 6000.00 * (1 - 0.0020) = 5988.00
kr_taker_bid * (1 - taker_fee) = 6003.6094 * (1 - 0.0026) = 5988.00001556

# -- Market Making ---------------------------------------------------------------------------------------- # 
# --------------------------------------------------------------------------------------------------------- # 

On Destination, Make a BID to BUY 1 BTC @kr_maker_bid, On Origin, take an existing BID to SELL @5,964.00

Make : BID @maker_bid to BUY 1 BTC on Kraken
Take : ASK @6000 to SELL 1 BTC on Bitfinex

We have the following model:

    kr_maker_bid * (1 + kr_maker_fee) = bf_taker_bid * (1 - bf_taker_fee)

By replacing the numbers we know leads to:

    kr_maker_bid * (1 + 0.0016) - 5964.00 * (1 - 0.0020) = 0

And so, the formula to get the final result is:
    
    kr_maker_bid = (5964.00 * (1 - 0.0020)) / (1 + 0.0016)

Finally, the BID to use as a Maker on Kraken, that leads to a 0 profit result, is:

    kr_maker_bid = 5942.563897764

Here are the final values:

    kr_ASK = 6021.6346
    kr_BID = 5942.563897764
    kr_SPREAD = 6021.6346 - 5942.563897764 = 79.070702236 or 131.31103 bp

    kr_maker_bid * (1 + kr_maker_fee) - bf_taker_bid * (1 - bf_taker_fee) = 0
    5942.563897764 * (1 + 0.0016) - 5964.00 * (1 - 0.0020) = 0

That means, the minimum spread we could hold on Kraken is: 79.0707 EUR or 131.3110 BP with respect ASK

Numerical proof:

    Make a BID in Kraken, then Take BID in Bitfinex
    kr_maker_bid * (1 + kr_maker_fee) = bf_taker_bid * (1 - bf_taker_fee)
    5942.5638 * (1 + 0.0016) = 5964.00 * (1 - 0.0020) = 0

    Take an ASK on Bitfinex, then Make an ASK in Kraken
    bf_taker_bid * (1 + bf_taker_fee) = kr_maker_ask * (1 - kr_maker_fee)
    6000 * (1 + 0.0020) - 6021.6346 * (1 - 0.0016) = 0
