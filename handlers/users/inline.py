# -*- coding: utf-8 -*-
from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, InlineQueryResultArticle

from loader import dp
from loader import db1
from random import randint


@dp.inline_handler(text="Search")
async def query(query: types.InlineQuery):
    title = [i for i in db1.select_all_users()]
    await query.answer(
        results=[
            types.InlineQueryResultArticle(
                id=str(randint(1, 500)),
                title=title[j][0],
                input_message_content=types.InputTextMessageContent(
                    message_text=title[j][1]))
            for j in range(len(title))])


@dp.message_handler(text="Посмотреть отправленные ранее посты")
async def user(message: types.Message):
    await message.answer("Инлайн режим",
                         reply_markup=InlineKeyboardMarkup(
                             inline_keyboard=[
                                 [
                                     InlineKeyboardButton(text="Войти в режим",
                                                          switch_inline_query_current_chat="Search")
                                 ]
                             ]
                         ))

