import requests
import datetime

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
