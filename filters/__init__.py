from aiogram import Dispatcher

from .private_chat import IsPrivate
from .administrator import Admin


def setup(dp: Dispatcher):
    dp.filters_factory.bind(IsPrivate)
