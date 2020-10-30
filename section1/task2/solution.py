# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
import pandas as pd
from binance.client import Client


# %%
class Binance:
    def __init__(self, symbol):
        self.client = Client()
        self.symbol = symbol

    def get_candle(self, start_time, end_time=None):
        candle = self.client.get_historical_klines(self.symbol, Client.KLINE_INTERVAL_30MINUTE, start_time, end_str=end_time)
        df = pd.DataFrame(candle, columns = ["Open timestamp", "Open", "High", "Low", "Close", "Volume", "Close timestamp", "Quote asset volume", "Number of    trades", "Taker buy base asset volume", "Taker buy quote asset volume", "Can be ignored"])
        df['Open time'] = pd.to_datetime(df['Open timestamp'],unit='ms')
        df['Close time'] = pd.to_datetime(df['Close timestamp'],unit='ms')
        df = df[['Open time', 'Open','High','Low','Close','Volume','Close time']]
        df.to_csv('./candle_data.csv', index=False)


    def get_recent_transactions(self, limit=50):
        transactions = self.client.get_recent_trades(symbol=self.symbol, limit=limit)
        df = pd.DataFrame(transactions)
        df['Datetime'] = pd.to_datetime(df['time'],unit='ms')
        df.rename(columns = { "id": "ID", "price": "Price", "qty": "Quantity", "quoteQty": "QuoteQuantity", "time": "Time", "isBuyerMaker": "Buyer maker", "isBestMatch": "Best match"}, inplace=True)
        df.to_csv('./recent_transactions.csv', index=False)

    def get_market_depth(self, limit=50):
        depth = self.client.get_order_book(symbol=self.symbol, limit=limit)
        bids = pd.DataFrame(depth['bids'], columns=["Price", "Quantity"])
        bids['Type'] = "Bid"
        asks = pd.DataFrame(depth['asks'], columns=["Price", "Quantity"])
        asks['Type'] = "Ask"
        df = pd.concat([bids,asks])
        df.to_csv('./market_depth.csv', index=False)


# %%
binance = Binance("BNBBTC")
binance.get_candle(start_time="2020-10-29T01:16:04.568Z")
binance.get_recent_transactions(limit=100)
binance.get_market_depth(limit=100)


# %%



