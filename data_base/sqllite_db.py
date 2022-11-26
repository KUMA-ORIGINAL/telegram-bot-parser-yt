import sqlite3 as sq
from create_bot import bot
from parse import parser


def sql_start():
    global base, cur
    base = sq.connect('YT.db')
    cur = base.cursor()
    if base:
        print('База данных подключилась')
    base.execute('CREATE TABLE IF NOT EXISTS videos(id INTEGER PRIMARY KEY AUTOINCREMENT,link TEXT, name_channel TEXT,\
                 subscribers TEXT, name_video TEXT, number_views TEXT, number_likes TEXT)')
    base.commit()


async def sql_add_command(state):
    async with state.proxy() as data:
        cur.execute('INSERT INTO videos(link, name_channel, subscribers, name_video, number_views, number_likes) \
        VALUES (?, ?, ?, ?, ?, ?)', tuple(parser.get_info(data['link'])))
        base.commit()


async def sql_read(message):
    for ret in cur.execute('SELECT * FROM videos').fetchall():
        await bot.send_message(message.from_user.id, f'{ret[1]}\nНомер видео: {ret[0]}\nКанал: {ret[2]}\nПодписчики'
                                                     f': {ret[3]}\nНазвание видео: {ret[4]}\nПросмотры:'
                                                     f' {ret[5]}\nЛайки:'
                                                     f' {ret[6]}\n')


async def sql_read2():
    return cur.execute('SELECT * FROM videos').fetchall()


async def sql_delete_command(data):
    cur.execute('DELETE FROM videos WHERE id == ?', (data,))
    base.commit()
