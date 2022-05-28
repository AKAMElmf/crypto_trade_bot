from crypto_api import api_cryp


def change_coins_amount(usdt_amount, coin):
    if coin == 'BTC':
        coin_amount = float(usdt_amount) / float(api_cryp.get_ticker()[0])
        return coin_amount.__round__(7)
    elif coin == 'ETH':
        coin_amount = float(usdt_amount) / float(api_cryp.get_ticker()[1])
        return coin_amount.__round__(7)
    else:
        print('error')


def change_usdt_amount(coin_amount, coin):
    if coin == 'BTC':
        usdt_amount = float(coin_amount) * float(api_cryp.get_ticker()[0])
        return usdt_amount.__round__(2)
    elif coin == 'ETH':
        usdt_amount = float(coin_amount) * float(api_cryp.get_ticker()[1])
        return usdt_amount.__round__(2)
    else:
        print('error')


def check_balance(usdt_bal, usdt_to_crypto):
    try:
        if (float(usdt_bal) - float(usdt_to_crypto)) >= 0 and check_message(usdt_to_crypto):
            return 0
        elif (float(usdt_bal) - float(usdt_to_crypto)) < 0:
            return 1
    except:
        return 2


def check_crypto_balance(crypto_bal, crypto_to_sell):
    try:
        if (float(crypto_bal) - float(crypto_to_sell)) >= 0 and check_message(crypto_to_sell):
            return 0
        elif (float(crypto_bal) - float(crypto_to_sell)) < 0:
            return 1
    except:
        return 2


def check_message(message):
    try:
        if float(message) > 0:
            return True
    except:
        return False


def check_crypto_name(coin):
    global i
    if coin == 'BTC':
        i = 0
        return i
    elif coin == 'ETH':
        i = 1
        return i
    else:
        print('error')


def check_zeroes(balance):
    if float(balance) == 0.0:
        return True
    else:
        return False


def tokens_price(btc_amount, eth_amount):
    price = ((float(api_cryp.get_ticker()[0]) * float(btc_amount)) +
             (float(api_cryp.get_ticker()[1]) * float(eth_amount))).__round__(2)
    if price == 0.0:
        price = 0
    return str(price)
