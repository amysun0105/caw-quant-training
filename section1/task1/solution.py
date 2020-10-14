# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
import datetime
start_time="2017-04-01"
end_time="2020-04-01"
start_timestamp = datetime.datetime.strptime(start_time, '%Y-%m-%d').replace(tzinfo=datetime.timezone.utc).timestamp()
end_timestamp = datetime.datetime.strptime(end_time, '%Y-%m-%d').replace(tzinfo=datetime.timezone.utc).timestamp()


# %%
import requests
url = 'https://min-api.cryptocompare.com/data/v2/histohour'
params = {
    'fsym': 'BTC',
    'tsym': 'USDT',
    'e': 'binance',
    'toTs': end_timestamp,
    'limit': 2000
}
response = requests.get(url, params=params).json()
last_timestamp = response['Data']['TimeFrom']
data = response['Data']['Data']


# %%
import pandas as pd
df = pd.DataFrame(data)
df['datetime'] = pd.to_datetime(df['time'],unit='s')
df.tail()


# %%
while (last_timestamp > start_timestamp):
    params = {
        'fsym': 'BTC',
        'tsym': 'USDT',
        'e': 'binance',
        'toTs': last_timestamp - 1,
        'limit': 2000
    }
    response = requests.get(url, params=params).json()
    last_timestamp = response['Data']['TimeFrom']
    data = response['Data']['Data'] + data


# %%
df = pd.DataFrame(data)
df = df[df.time >= start_timestamp]
df['datetime'] = pd.to_datetime(df['time'],unit='s')
df.drop(columns=['time', 'conversionType', 'conversionSymbol'], inplace=True)
df.rename(columns={'volumefrom': 'volume', 'volumeto': 'baseVolume'}, inplace=True)
df.tail()


# %%
df.head()


# %%
df.to_csv('./output.csv', index=False)


