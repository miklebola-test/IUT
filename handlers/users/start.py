import sqlite3

from aiogram import types
from aiogram.dispatcher.filters.builtin import Command
from loader import dp, bot, db, db1

chat_id = 1069992966

@dp.message_handler(Command('start'))
async def new_post(message: types.Message):
    name = message.from_user.full_name
    await bot.send_photo(chat_id=message.chat.id,
                         photo='https://sun9-26.userapi.com/impg/u5v_B5B37xeG8lakUj59OFD4HMgOjOg4Kb6yUw/Jcx4kDtKQbk.jpg?size=1200x1200&quality=96&proxy=1&sign=4b8a15e2e45fb2960f856e4fd0c2c8d0&type=album',
                         caption='Шалом петушки')
    try:
        db.add_user(id=message.from_user.id, name=name)
    except sqlite3.IntegrityError as err:
        print(err)

    count_users = db.count_users()[0]
    await message.answer(
        f'В базе <b>{count_users}</b> пользователей'
    )
    b = [i for i in db1.select_all_users()]
    for j in range(len(b)):
        await message.answer(b[j][0])



