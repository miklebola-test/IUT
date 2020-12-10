from aiogram import types
from aiogram.dispatcher import FSMContext
from filters import IsPrivate, Admin
from loader import dp
from loader import bot
from states import Post

from data.config import admins


# В этом хендлере используем фильтры для приватной переписки,
# фильтр на точное совпадение по слову "secret"
# и только для использования пользователей в списке admins
@dp.message_handler(IsPrivate(), text="secret", user_id=admins)
async def admin_chat_secret(message: types.Message):
    await message.answer("Это секретное сообщение, вызванное одним из администраторов "
                         "в личной переписке")
    await Post.post.set()

# @dp.message_handler(state=Post.post)
async def new_post(message: types.Message, state: FSMContext):
    send_post = message.text
    await bot.send_message(chat_id=252304907, text=send_post)
    await state.finish()
