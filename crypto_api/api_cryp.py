import json
import requests


def get_ticker():
    crypto_price = []
    base = 'https://fapi.binance.com'
    path_ticker = '/fapi/v1/ticker/price'
    symb = ['BTCUSDT', 'ETHUSDT']
    for i in range(2):
        param = {'symbol': symb[i]}
        response = requests.get(url=base+path_ticker, params=param)
        if response.status_code == 200:
            data = response.text
            data = json.loads(data)
            crypto_price.append(str(data['price']))
        else:
            response = requests.get(url='https://yobit.net/api/3/ticker/btc_usdt-eth_usdt')
            data = response.text
            data = json.loads(data)
            crypto_price.append(str(float(data['btc_usdt']['last']).__round__(3)))
            crypto_price.append(str(float(data['eth_usdt']['last']).__round__(3)))
            break
    return crypto_price

