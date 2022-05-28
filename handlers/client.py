from aiogram import types, Dispatcher
from create_bot import bot
from keyboards import client_kb as kb
from database import sqlite_bd as db
from crypto_api import api_cryp as api
from others import funcs as f
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text


class FSMclient(StatesGroup):
    start_dep = State()
    amount_of_buy_crypto = State()
    amount_of_sell_crypto = State()
    reset_balance = State()
    yes_no_delete = State()


async def command_start(message: types.Message):
    if message.from_user.id == db.sql_read_id(message.from_user.id):
        await bot.send_message(message.from_user.id, 'Выберите действие',
                               reply_markup=kb.kb_main)
    else:
        await FSMclient.start_dep.set()
        await bot.send_message(message.from_user.id, 'Введите тестовый баланс в USDT',
                               reply_markup=kb.kb_cancel)


async def command_start_dep(message: types.Message, state: FSMContext):
    if f.check_message(message.text):
        db.sql_add_start(message.from_user.id, message.text)
        await bot.send_message(message.from_user.id, 'Тестовый баланс сохранен',
                               reply_markup=kb.kb_main)
        await state.finish()
    else:
        await bot.send_message(message.from_user.id, 'Вы ввели некорректное значение',
                               reply_markup=kb.kb_start)


async def command_balance(message: types.Message):
    await bot.send_message(message.from_user.id, 'Ваш баланс: ' +
                           str(db.sql_get_dep(message.from_user.id)) + ' USDT')


async def command_get_crypto(message: types.Message):
    crypto_list = db.sql_get_crypto(message.from_user.id)
    await bot.send_message(message.from_user.id, 'BTC: ' + str(crypto_list[0]) +
                           '\n' + 'ETH: ' + str(crypto_list[1])+'\nОбщая стоимость монет: ' +
                           f.tokens_price(db.sql_get_crypto(message.from_user.id)[0],
                                          db.sql_get_crypto(message.from_user.id)[1]) + ' USDT')


async def command_trade(message: types.Message):
    await bot.send_message(message.from_user.id, 'Выберите действие',
                           reply_markup=kb.kb_trade)


async def command_back(message: types.Message):
    await bot.send_message(message.from_user.id, 'Выберите действие',
                           reply_markup=kb.kb_main)


async def command_rate_crypto(message: types.Message):
    if message.text == 'Курс BTC':
        price = 'BTC: ' + api.get_ticker()[0] + ' USDT'
        await bot.send_message(message.from_user.id, price)
    elif message.text == 'Курс ETH':
        price = 'ETH: ' + api.get_ticker()[1] + ' USDT'
        await bot.send_message(message.from_user.id, price)
    else:
        await bot.send_message(message.from_user.id, 'Неправильная команда')


async def command_buy_crypto(message: types.Message, state: FSMContext):

    if message.text == 'Купить BTC':
        async with state.proxy() as data:
            data['coin'] = 'BTC'
        await FSMclient.amount_of_buy_crypto.set()
    elif message.text == 'Купить ETH':
        async with state.proxy() as data:
            data['coin'] = 'ETH'
        await FSMclient.amount_of_buy_crypto.set()
    else:
        await bot.send_message(message.from_user.id, 'Неправильная команда')
        await state.finish()
        return
    coin = data['coin']
    if f.check_zeroes(db.sql_get_dep(message.from_user.id)):
        await bot.send_message(message.from_user.id, 'У вас нет средств для покупки ' + coin,
                               reply_markup=kb.kb_trade)
        await state.finish()
        return
    await bot.send_message(message.from_user.id,
                           'Ваш баланс: ' + str(db.sql_get_dep(message.from_user.id)) + ' USDT')
    await bot.send_message(message.from_user.id, 'Введите сумму USDT',
                           reply_markup=kb.kb_cancel)


async def command_sell_crypto(message: types.Message, state: FSMContext):
    crypto_list = db.sql_get_crypto(message.from_user.id)
    if message.text == 'Продать BTC':
        async with state.proxy() as data:
            data['coin'] = 'BTC'
        await FSMclient.amount_of_sell_crypto.set()
        await bot.send_message(message.from_user.id, 'Ваше количество BTC: ' +
                               str(crypto_list[0]))
    elif message.text == 'Продать ETH':
        async with state.proxy() as data:
            data['coin'] = 'ETH'
        await FSMclient.amount_of_sell_crypto.set()
        await bot.send_message(message.from_user.id, 'Ваше количество ETH: ' +
                               str(crypto_list[1]))
    else:
        await bot.send_message(message.from_user.id, 'Неправильная команда')
        await state.finish()
        return
    coin = data['coin']
    i = f.check_crypto_name(coin)
    if f.check_zeroes(db.sql_get_crypto(message.from_user.id)[i]):
        await bot.send_message(message.from_user.id, 'У вас нет ' + coin + ' для продажи',
                               reply_markup=kb.kb_trade)
        await state.finish()
        return
    await bot.send_message(message.from_user.id, 'Введите количество монет',
                           reply_markup=kb.kb_cancel)


async def command_amount_of_buy_crypto(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        coin = data['coin']
    if f.check_balance(db.sql_get_dep(message.from_user.id), message.text) == 0:
        amount_of_buy = db.sql_buy_crypto(message.from_user.id, coin, message.text)
        balance = str(db.sql_get_dep(message.from_user.id))
        await bot.send_message(message.from_user.id, 'Покупка совершена\nВы купили: ' +
                               amount_of_buy + ' ' + coin +
                               '\nВаш баланс: ' + balance + ' USDT',
                               reply_markup=kb.kb_trade)
    elif f.check_balance(db.sql_get_dep(message.from_user.id), message.text) == 1:
        await bot.send_message(message.from_user.id, 'Недостаточный баланс',
                               reply_markup=kb.kb_trade)
    else:
        await bot.send_message(message.from_user.id, 'Вы ввели некорректное значение',
                               reply_markup=kb.kb_trade)
    await state.finish()


async def command_amount_of_sell_crypto(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        coin = data['coin']
    i = f.check_crypto_name(coin)
    if f.check_crypto_balance(db.sql_get_crypto(message.from_user.id)[i], message.text) == 0:
        amount_of_sell = db.sql_sell_crypto(message.from_user.id, coin, message.text)
        balance = str(db.sql_get_dep(message.from_user.id))
        await bot.send_message(message.from_user.id, 'Продажа совершена\nВы получили: ' +
                               amount_of_sell + ' USDT\n' +
                               'Ваш баланс: ' + balance + ' USDT' + '\nBTC: ' +
                               str(db.sql_get_crypto(message.from_user.id)[0]) +
                               '\nETH: ' + str(db.sql_get_crypto(message.from_user.id)[1]),
                               reply_markup=kb.kb_trade)
    elif f.check_crypto_balance(db.sql_get_crypto(message.from_user.id)[i], message.text) == 1:
        await bot.send_message(message.from_user.id, 'Недостаточный баланс',
                               reply_markup=kb.kb_trade)
    else:
        await bot.send_message(message.from_user.id, 'Вы ввели некорректное значение',
                               reply_markup=kb.kb_trade)
    await state.finish()


async def command_settings(message: types.Message):
    await bot.send_message(message.from_user.id, 'Выберите действие',
                           reply_markup=kb.kb_settings)


async def command_reset_balance(message: types.Message):
    await FSMclient.reset_balance.set()
    await bot.send_message(message.from_user.id, 'Введите новый тестовый баланс в USDT',
                           reply_markup=kb.kb_cancel)


async def reset_balance(message: types.Message, state: FSMContext):
    if f.check_message(message.text):
        db.sql_reset_balance(message.from_user.id, message.text)
        await bot.send_message(message.from_user.id, 'Тестовый баланс сохранен',
                               reply_markup=kb.kb_main)
    else:
        await bot.send_message(message.from_user.id, 'Вы ввели некорректное значение',
                               reply_markup=kb.kb_settings)
    await state.finish()


async def command_cancel(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if db.sql_read_id(message.from_user.id) != 0:
        if current_state is None:
            await bot.send_message(message.from_user.id, 'Выберите действие',
                                   reply_markup=kb.kb_main)
            return
        await bot.send_message(message.from_user.id, 'Выберите действие',
                               reply_markup=kb.kb_main)
        await state.finish()
    else:
        if current_state is None:
            await bot.send_message(message.from_user.id, 'Выберите действие',
                                   reply_markup=kb.kb_start)
            return
        await bot.send_message(message.from_user.id, 'Выберите действие',
                               reply_markup=kb.kb_start)
        await state.finish()


async def command_delete_acc(message: types.Message):
    await FSMclient.yes_no_delete.set()
    await bot.send_message(message.from_user.id, 'Вы уверены?',
                           reply_markup=kb.kb_yes_no)


async def yes_no_delete(message: types.Message, state: FSMContext):
    if message.text == 'Да':
        db.sql_delete_acc(message.from_user.id)
        await bot.send_message(message.from_user.id, 'Аккаунт успешно удален',
                               reply_markup=kb.kb_start)
        await state.finish()
    else:
        await bot.send_message(message.from_user.id, 'Удаление отменено',
                               reply_markup=kb.kb_main)
        await state.finish()


def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(command_start, commands=['start'], state=None)
    dp.register_message_handler(command_balance, lambda message: 'Баланс' in message.text)
    dp.register_message_handler(command_get_crypto, lambda message: 'Монеты' in message.text)
    dp.register_message_handler(command_trade, lambda message: 'Торговля' in message.text)
    dp.register_message_handler(command_rate_crypto, lambda message: 'Курс' in message.text)
    dp.register_message_handler(command_buy_crypto, lambda message: 'Купить' in message.text, state=None)
    dp.register_message_handler(command_sell_crypto, lambda message: 'Продать' in message.text, state=None)
    dp.register_message_handler(command_reset_balance, lambda message: 'Сбросить баланс' in
                                                                       message.text, state=None)
    dp.register_message_handler(command_cancel, state="*", commands=['Отмена'])
    dp.register_message_handler(command_cancel, Text(equals='Отмена', ignore_case=True), state="*")
    dp.register_message_handler(command_start_dep, content_types=['text'], state=FSMclient.start_dep)
    dp.register_message_handler(reset_balance, content_types=['text'], state=FSMclient.reset_balance)
    dp.register_message_handler(command_amount_of_buy_crypto, content_types=['text'],
                                state=FSMclient.amount_of_buy_crypto)
    dp.register_message_handler(command_amount_of_sell_crypto, content_types=['text'],
                                state=FSMclient.amount_of_sell_crypto)
    dp.register_message_handler(command_back, lambda message: 'Назад' in message.text)
    dp.register_message_handler(command_settings, lambda message: 'Настройки' in message.text)
    dp.register_message_handler(command_delete_acc, lambda message: 'Удалить данные' in message.text, state=None)
    dp.register_message_handler(yes_no_delete, lambda message: 'Да' or 'Нет' in message.text,
                                state=FSMclient.yes_no_delete)
