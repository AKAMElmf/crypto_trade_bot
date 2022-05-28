from aiogram.utils import executor
from create_bot import dp
from database import sqlite_bd

def on_startup( ):
    print('Бот вышел в онлайн')
    sqlite_bd.sql_start()

from handlers import client, other

client.register_handlers_client(dp)
other.register_handlers_other(dp)

executor.start_polling(dp, on_startup=on_startup())
executor.start_polling(dp, skip_updates=True)






