from aiogram import types, Dispatcher
from database import sqlite_bd as db
from keyboards import client_kb as kb


async def other(message: types.Message):
    if db.sql_read_id(message.from_user.id) != 0:
        await message.answer('Такой команды нет')
        await message.delete()
    else:
        await message.answer('Введите команду /start для начала торговли', reply_markup=kb.kb_start)


def register_handlers_other(dp: Dispatcher):
    dp.register_message_handler(other)
