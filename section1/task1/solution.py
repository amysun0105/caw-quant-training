# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
import datetime
import requests
import pandas as pd

HISTOHOUR = 'https://min-api.cryptocompare.com/data/v2/histohour'

def get_histohour(fsym, tsym, start_time='2017-04-01', end_time='2020-04-01', e='binance'):
    start_timestamp = datetime.datetime.strptime(start_time, '%Y-%m-%d').replace(tzinfo=datetime.timezone.utc).timestamp()
    end_timestamp = datetime.datetime.strptime(end_time, '%Y-%m-%d').replace(tzinfo=datetime.timezone.utc).timestamp()
    last_timestamp = end_timestamp + 1
    data = []

    while (last_timestamp > start_timestamp):
        params = {
            'fsym': fsym,
            'tsym': tsym,
            'e': e,
            'toTs': last_timestamp - 1,
            'limit': 2000
        }
        response = requests.get(HISTOHOUR, params=params).json()
        last_timestamp = response['Data']['TimeFrom']
        data = response['Data']['Data'] + data

    df = pd.DataFrame(data)
    df = df[df.time >= start_timestamp]
    df['datetime'] = pd.to_datetime(df['time'],unit='s')
    df.drop(columns=['time', 'conversionType', 'conversionSymbol'], inplace=True)
    df.rename(columns={'volumefrom': 'volume', 'volumeto': 'baseVolume'}, inplace=True)
    df.to_csv('./output.csv', index=False)


# %%
get_histohour('BTC', 'USDT')


