from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

b1 = KeyboardButton('/Добавить_видео')
b2 = KeyboardButton('/Список_видео')
b3 = KeyboardButton('/Удалить_видео')

kb_client = ReplyKeyboardMarkup(resize_keyboard=True)

kb_client.row(b1, b3).add(b2)
