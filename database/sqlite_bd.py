import sqlite3 as sq
from others import funcs as f


def sql_start():
    global base, cur
    base = sq.connect('bd_crypto_users.db')
    cur = base.cursor()
    if base:
        print('BD connected')
    base.execute('CREATE TABLE IF NOT EXISTS {}(id PRIMARY KEY, USDT,BTC,ETH)'.format('data'))
    base.commit()


def sql_add_start(user_id, usdt):
    cur.execute('INSERT INTO data VALUES (?,?,?,?)', (user_id, str(usdt), str(0), str(0)))
    base.commit()


def sql_reset_balance(user_id, usdt):
    cur.execute('UPDATE data SET BTC == 0, ETH == 0 WHERE id == ' +
                str(user_id))
    base.commit()
    cur.execute('UPDATE data SET USDT == ' + str(usdt) +
                ' WHERE id == ' + str(user_id))
    base.commit()


def sql_get_dep(user_id):
    r = cur.execute('SELECT USDT FROM data WHERE id LIKE \'%' +
                    str(user_id) + '%\'').fetchone()
    return r[0]


def sql_get_crypto(user_id):
    r = cur.execute('SELECT BTC, ETH FROM data WHERE id LIKE \'%' +
                    str(user_id) + '%\'').fetchone()
    return r


def sql_buy_crypto(user_id, coin, usdt):
    i = f.check_crypto_name(coin)
    amount_of_crypto = float(f.change_coins_amount(usdt, coin)).__round__(7)
    cur.execute('UPDATE data SET ' + coin + ' == ' +
                str((float(sql_get_crypto(user_id)[i]).__round__(7) +
                     amount_of_crypto)) +
                ' WHERE id == ' + str(user_id))
    base.commit()
    amount_of_usdts = (float(sql_get_dep(user_id)) - float(usdt)).__round__(2)
    if amount_of_usdts == 0.0:
        amount_of_usdts = 0
    cur.execute('UPDATE data SET USDT == ' + str(amount_of_usdts) +
                ' WHERE id == ' + str(user_id))
    base.commit()
    return str(amount_of_crypto)


def sql_sell_crypto(user_id, coin, crypto_amount):
    i = f.check_crypto_name(coin)
    crypto_balance = (float(sql_get_crypto(user_id)[i]) - float(crypto_amount)).__round__(7)
    if crypto_balance == 0.0:
        crypto_balance = 0
    cur.execute('UPDATE data SET ' + coin + ' == ' + str(crypto_balance) +
                ' WHERE id == ' + str(user_id))
    base.commit()
    usdt_amount = float(f.change_usdt_amount(crypto_amount, coin)).__round__(2)
    cur.execute('UPDATE data SET USDT == ' + str(
        (float(sql_get_dep(user_id)).__round__(2) +
         usdt_amount)) + ' WHERE id == ' + str(user_id))
    base.commit()
    return str(usdt_amount)


def sql_delete_acc(user_id):
    cur.execute('DELETE FROM data WHERE id == ' +
                str(user_id))
    base.commit()


def sql_read_id(user_id):
    try:
        r = cur.execute('SELECT id FROM data WHERE id LIKE \'%' +
                        str(user_id) + '%\'').fetchone()
        return r[0]
    except:
        return 0
