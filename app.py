import requests
import os, csv
import datetime 
import pandas as pd
import numpy as np
import talib
from patterns import candlestick_patterns
from binance import Client

from flask import Flask, render_template, request, render_template_string


client=Client()

def get_binance_data(ticker="BTC", interval="1h", start="2 days ago UTC"):
    ticker=ticker + "USDT"
    candles=client.get_historical_klines(symbol=ticker, interval=interval, start_str=start)
    data = pd.DataFrame(candles)
    data.columns = ['open_time','open', 'high', 'low', 'close', 'volume','close_time', 'qav','num_trades','taker_base_vol','taker_quote_vol', 'ignore']
    data['open_datetime'] = [pd.to_datetime(x, unit='ms').strftime('%Y-%m-%d %H:%M:%S') for x in data.open_time]
    data = data.drop(['open_time', 'volume','close_time', 'qav','num_trades','taker_base_vol','taker_quote_vol', 'ignore'], axis = 1)
    data = data.set_index('open_datetime')
    data = data.astype('float')
    return data

app = Flask(__name__)

@app.route("/")
def index():
    pattern = request.args.get("pattern", None)
    coins = {} 

    with open('datasets/coins.csv') as f:
        for row in csv.reader(f):
            coins[row[0]] = {'Coin Name': row[1]}

    if pattern:
        datafiles = os.listdir('datasets/hourly')
        for dataset in datafiles:
            df = pd.read_csv('datasets/hourly/{}'.format(dataset), index_col='open_datetime')
            pattern_function = getattr(talib, pattern)

            symbol = dataset.split('.')[0]
            try: 
                result = pattern_function(df['open'], df['high'], df['low'], df['close'])
                last = result.tail(1).values[0]
                if last > 0:
                    coins[symbol][pattern] = "Bullish"
                elif last < 0:
                    coins[symbol][pattern] = "Bearish"
                else:
                    coins[symbol][pattern] = None
            except:
                pass
    return render_template("index.html", patterns=candlestick_patterns, stocks=coins, current_pattern=pattern)

@app.route("/snapshot")
def snapshot():
    with open('datasets/coins.csv') as f:
        coins = f.read().splitlines()
        for coin in coins:
            symbol = coin.split(",")[0]
            binance_df = get_binance_data(symbol)
            binance_df.to_csv("datasets/hourly/{}.csv".format(symbol), index = True)
        
        return{
            "code": "success"
        }

def snapshot_handler():
    snapshot()
    return 'Snapshot completed'


if __name__ == "__main__": 
    app.run(host="0.0.0.0", debug=True)

'''
def get_crypto_data():
    url = 'https://min-api.cryptocompare.com/data/v2/histohour'
    payload = {
        'fsym': input('Enter crypto currency symbol: '),
        'tsym': 'USD',
        'limit': '20',
        'toTs': '-1',
        'api_key': 'a03c921d1d62d2ee5d7fce9351271e0d2f3dc85f735173eb30c66a60b57241a0'
    }
    response = requests.get(url, params=payload)
    json = response.json()
    data = json['Data']['Data']
    times = [obj['time'] for obj in data]
    prices = [obj['high'] for obj in data]
    txt = ""
    for i in range(len(times)):
        txt += f"{times[i]}\t{serial_date_to_nice_date(times[i]/3600/24).strftime('%Y-%m-%d %H:%M:%S')}\t{prices[i]}\n"
    print(txt)
    print(f"From Time: {times[0]}")
    print(f"To Time: {times[-1]}")
    print(f"From Info: ({serial_date_to_nice_date(times[0]/3600/24).strftime('%Y-%m-%d %H:%M:%S')})")
    print(f"To Info: ({serial_date_to_nice_date(times[-1]/3600/24).strftime('%Y-%m-%d %H:%M:%S')})")

def get_btc_data_previous():
    url = 'https://min-api.cryptocompare.com/data/v2/histohour'
    payload = {
        'fsym': input('Enter crypto currency symbol: '),
        'tsym': 'USD',
        'limit': '2000',
        'toTs': input('Enter from time: '),
        'api_key': 'YOURAPIKEY'
    }
    response = requests.get(url, params=payload)
    json = response.json()
    data = json['Data']['Data']
    times = [obj['time'] for obj in data]
    prices = [obj['high'] for obj in data]
    txt = ""
    for i in range(len(times)):
        txt += f"{times[i]}\t{serial_date_to_nice_date(times[i]/3600/24).strftime('%Y-%m-%d %H:%M:%S')}\t{prices[i]}\n"
    tmp = input('Enter previous data: ')
    print(txt + tmp)
    print(f"From Time: {times[0]}")
    print(f"To Time: {times[-1]}")
    print(f"From Info: ({serial_date_to_nice_date(times[0]/3600/24).strftime('%Y-%m-%d %H:%M:%S')})")
    print(f"To Info: ({serial_date_to_nice_date(times[-1]/3600/24).strftime('%Y-%m-%d %H:%M:%S')})")

def serial_date_to_nice_date(date):
    return datetime.datetime.fromtimestamp(date * 86400).replace(hour=0, minute=0, second=0)

get_crypto_data()
'''