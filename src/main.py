import gdax
from threading import Thread


class CryptoAribtrage():
    def __init__(self, auth_client=False, API_key=None, API_secret=None, API_pass=None, API_url=None):
        if auth_client:
            self.authClient = gdax.AuthenticatedClient(API_key, API_secret, API_pass, API_url)
        else:
            self.authClient = False
        self.publicClient = gdax.PublicClient()

    def trade(self, dollars, threshold=1.01, execute=False):

        execute = False if not self.authClient else execute

        def execute_trade(dollars, buy_currency, sell_currency, exchange_currency, execute=False):

            def next_order():
                while True:
                    orders = self.authClient.get_orders()
                    order_book = []
                    for order_currency in orders:
                        if len(order_currency) == 0:
                            return True
                        for order in order_currency:
                            try:
                                order_book.append(order['settled'])
                            except:
                                continue
                        if all(order_book):
                            return True
                return False

            buyParams = {'price': str(buy_currency[1]),
                         'size': str(round(dollars / buy_currency[1], 8)),
                         'product_id': buy_currency[0]
                         }

            Xparams = {'price': str(round(exchange_currency[1], 8)),
                       'size': str(round(dollars / buy_currency[1], 8)),
                       'product_id': exchange_currency[0]
                       }

            sellParams = {'price': str(sell_currency[1]),
                          'size': str(round((dollars / buy_currency[1]) * exchange_currency[1], 8)),
                          'product_id': sell_currency[0]
                          }


            if execute:
                self.authClient.buy(buyParams)
                if next_order():
                    if buy_currency[0] == "BTC-USD":
                        self.authClient.sell(Xparams)
                    else:
                        self.authClient.buy(Xparams)
                if next_order():
                    self.authClient.sell(sellParams)

            print(buyParams)
            print(Xparams)
            print(sellParams)

        def get_quotes(tickers, quotes=None):
            if quotes is None:
                quotes = {}
            for ticker in tickers:
                quotes[ticker] = self.publicClient.get_product_ticker(product_id=ticker)


        def threaded_process(nthreads, products):

            quotes = {}
            threads = []

            for i in range(nthreads):
                tickers = products[i::nthreads]
                t = Thread(target=get_quotes, args=(tickers, quotes))
                threads.append(t)

            [t.start() for t in threads]
            [t.join() for t in threads]
            return quotes

        while True:

            products = ["ETH-USD", "BTC-USD", "ETH-BTC"]
            quotes = threaded_process(3, products)
            ETH = quotes["ETH-USD"]
            BTC = quotes["BTC-USD"]
            ETH_BTC = quotes["ETH-BTC"]

            ETH_bid = float(ETH['bid'])
            ETH_ask = float(ETH['ask'])

            BTC_bid = float(BTC['bid'])
            BTC_ask = float(BTC['ask'])

            ETH_BTC_bid = float(ETH_BTC['bid'])
            ETH_BTC_ask = float(ETH_BTC['ask'])

            buy_BTC_arb = (ETH_bid / ETH_BTC_ask) / BTC_ask
            buy_ETH_arb = BTC_bid * ETH_BTC_bid / ETH_ask


            if buy_BTC_arb > threshold:
                buy_currency = ('BTC-USD', BTC_ask)
                sell_currency = ('ETH-USD', ETH_bid)
                exchange_currency = ('ETC-BTC', 1 / ETH_BTC_ask)
                execute_trade(dollars, buy_currency, sell_currency,
                              exchange_currency)
                break
            if buy_ETH_arb > threshold:
                buy_currency = ('ETH-USD', ETH_ask)
                sell_currency = ('BTC-USD', BTC_bid)
                exchange_currency = ('ETC-BTC', ETH_BTC_bid)
                execute_trade(dollars, buy_currency, sell_currency,
                              exchange_currency)
                break
    def cancel_trades(self):
        orders = self.authClient.get_orders()
        for order in orders:
            try:
                self.authClient.cancel_order(order[0])
            except Exception as e:
                print(e)

"""
Set threshold as a decimal here. 0.004 is 40 basis points.
"""
if __name__ == "__main__":

    tradebot = CryptoAribtrage(False)
    publicClient = gdax.PublicClient()
    threshold = 0.000
    tradebot.trade(1, 1 + threshold)
