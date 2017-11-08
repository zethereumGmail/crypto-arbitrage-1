# crypto-arbitrage
Algorithm for exploiting triangular arbitrage in crypto currency market.

To use:

Initialize the CrytoArbitrage class with an API Key, API_key, API_secret, API_pass, and API_url from your GDAX account. If you do not provide a key, the program will still track exchange rates using the public client, but will just print out trade orders rather than execute them.

Use CrytoArbitrage.trade to begin scanning for arbitrage opportunities. If you do not select a threshold value, i.e. the minimum arbitrage value at which to execute the trade, it will default to 100 BPS. It is recommended to set the threshold above the trading costs, which are 25 BPS per trade so 75 BPS for a complete arbitrage cycle.
