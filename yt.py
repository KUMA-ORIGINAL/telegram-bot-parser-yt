from aiogram import types, executor
from create_bot import dp
from handlers import client
from data_base import sqllite_db


async def on_startup(_):
    print('Бот вышел в чат')
    sqllite_db.sql_start()


client.register_handlers_client(dp)


@dp.message_handler()
async def a(message: types.Message):
    await message.answer(message.text)

executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
