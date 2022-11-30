from aiogram import types, Dispatcher

from create_bot import bot
from keyboards import kb_client
from data_base import sqllite_db

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


async def start(message: types.Message):
    try:
        await bot.send_message(message.from_user.id, 'Че надо?', reply_markup=kb_client.kb_client)
        await message.delete()
    except:
        await message.reply('Общение с ботом через ЛС, напишите ему: \nhttps://t.me/yt_parse_yt_bot')


class FSM(StatesGroup):
    link = State()


async def add_video(message: types.Message):
    await FSM.link.set()
    await message.reply("Отправьте ссылку видео")


async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.reply('OK')


async def load_link(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['link'] = message.text
    await message.reply('Подождите 25 секунд')
    await sqllite_db.sql_add_command(state)
    await state.finish()
    await message.answer('Успешно добавилось')


async def list_videos(message: types.Message):
    if await sqllite_db.sql_read(message) is None:
        await message.answer('Нету добавленных видео')
    else:
        await sqllite_db.sql_read(message)


async def del_callback_run(callback_query: types.CallbackQuery):
    await sqllite_db.sql_delete_command(callback_query.data.replace('del ', ''))
    await callback_query.answer(text=f'видео номер {callback_query.data.replace("del ", "")} удалена.', show_alert=True)


async def delete_item(message: types.Message):
    read = await sqllite_db.sql_read2()
    for ret in read:
        await bot.send_message(message.from_user.id, f'{ret[1]}\nНомер видео: {ret[0]}\nКанал: {ret[2]}\nПодписчики'
                                                     f':{ret[3]}\nНазвание видео: {ret[4]}\nПросмотры: {ret[5]}\nЛайки:'
                                                     f' {ret[6]}\n')
        await bot.send_message(message.from_user.id, text='---', reply_markup=InlineKeyboardMarkup().add(
            InlineKeyboardButton(f'Удалить видео {ret[0]}', callback_data=f'del {ret[0]}')))


def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(start, commands=['start', 'help'])
    dp.register_message_handler(add_video, commands=['Добавить_видео'])
    dp.register_message_handler(cancel_handler, state="*", commands=['отмена'])
    dp.register_message_handler(cancel_handler, Text(equals='отмена', ignore_case=True), state="*")
    dp.register_message_handler(load_link, state=FSM.link)
    dp.register_message_handler(list_videos, commands=['Список_видео'])
    dp.register_callback_query_handler(del_callback_run, lambda x: x.data and x.data.startswith('del '))
    dp.register_message_handler(delete_item, commands=['Удалить_видео'])
