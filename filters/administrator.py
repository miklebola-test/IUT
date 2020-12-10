from aiogram import types
from aiogram.dispatcher.filters import BoundFilter

from loader import bot

from data.config import admins


class Admin(BoundFilter):
    async def check(self, message: types.Message):
        await bot.get_chat_member(message.chat.id, message.from_user.id)
        return message.from_user.id in admins

