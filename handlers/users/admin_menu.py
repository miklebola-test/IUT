from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.types import ReplyKeyboardRemove, ContentType, Message
from data.config import admins

import sqlite3
from filters import Admin
from keyboards.default import menu, yes_no, view, back
from loader import dp, bot, db, db1
from states import Post

dp.message_handler(text="/teamaccess")


async def admini(message: types.Message):
    admins.append(message.from_user.id)


@dp.message_handler(Admin(), Command('teamaccess'))
async def show_menu(message: types.Message):
    await message.answer('Выберете один из пунктов меню', reply_markup=menu)


@dp.message_handler(Admin(), text='Написать новый пост')
async def new_post(message: types.Message):
    await message.answer(text=' Введите название поста для быстрого доступа к истории в дальнейшем',
                         reply_markup=ReplyKeyboardRemove())
    await Post.name.set()


@dp.message_handler(state=Post.name)
async def new_post(message: types.Message, state: FSMContext):
    post_name = message.text
    await state.update_data(post_name=post_name)
    await message.answer('Введите текст поста')
    await Post.post_body.set()


@dp.message_handler(state=Post.post_body)
async def new_post(message: types.Message, state: FSMContext):
    post_body = message.text
    await state.update_data(post_body=post_body)
    await message.answer('Прикрепить картинку к посту?', reply_markup=yes_no)
    await Post.photo.set()


@dp.message_handler(state=Post.photo, text='Да')
async def new_post(message: types.Message, state: FSMContext):
    await bot.send_message(chat_id=message.chat.id, text='Прикрепите картинку для поста',
                           reply_markup=ReplyKeyboardRemove())
    await Post.photo_yes.set()


@dp.message_handler(state=Post.photo_yes, content_types=ContentType.PHOTO)
async def answer(message: Message, state: FSMContext):
    photo_post = message.photo[-1].file_id
    await state.update_data(photo_post=photo_post)
    await message.answer('Фотография успешно добавлена')
    await bot.send_message(chat_id=message.chat.id, text='Выберте нужный вариант', reply_markup=view)


@dp.message_handler(state=Post.photo_yes, text='Предпросмотр')
async def answer(message: types.Message, state: FSMContext):
    data = await state.get_data()
    name_post = data.get('post_name')
    body_post = data.get('post_body')
    photo_post = data.get('photo_post')
    post_text = name_post + '\n' + body_post
    await bot.send_photo(chat_id=message.chat.id, photo=photo_post, caption=post_text)


@dp.message_handler(state=Post.photo_yes, text='Отправить')
async def answer(message: types.Message, state: FSMContext):
    data = await state.get_data()
    name_post = data.get('post_name')
    body_post = data.get('post_body')
    photo_post = data.get('photo_post')
    post_text = name_post + '\n' + body_post
    await bot.send_message(message.chat.id, text='Пост успешно отправлен', reply_markup=ReplyKeyboardRemove())
    for member in db.select_all_users():
        await bot.send_photo(chat_id=member[0], photo=photo_post, caption=post_text,
                             reply_markup=ReplyKeyboardRemove())
    try:
        db1.add_user(id=name_post, name=body_post)
    except sqlite3.IntegrityError as err:
        print(err)

    await state.finish()


@dp.message_handler(state=Post.photo, text='Нет')
async def new_post(message: types.Message, state: FSMContext):
    await bot.send_message(chat_id=message.chat.id, text='Пост будет отправлен без картиники',
                           reply_markup=ReplyKeyboardRemove())
    await bot.send_message(chat_id=message.chat.id, text='Отображать превью ссылок?', reply_markup=yes_no)
    await Post.choise.set()


@dp.message_handler(state=Post.choise, text='Нет')
async def new_post(message: types.Message, state: FSMContext):
    await bot.send_message(chat_id=message.chat.id, text='Превью ссылок не будут отображаться',
                           reply_markup=view)
    await message.answer('Выберете нужный вариант')
    await Post.photo_no_preview_no.set()


@dp.message_handler(state=Post.photo_no_preview_no, text='Предпросмотр')
async def answer(message: types.Message, state: FSMContext):
    data = await state.get_data()
    name_post = data.get('post_name')
    body_post = data.get('post_body')
    post_text = name_post + '\n' + body_post
    await message.answer(post_text, disable_web_page_preview=True)


@dp.message_handler(state=Post.photo_no_preview_no, text='Отправить')
async def answer(message: types.Message, state: FSMContext):
    data = await state.get_data()
    name_post = data.get('post_name')
    body_post = data.get('post_body')
    post_text = name_post + '\n' + body_post
    await bot.send_message(message.chat.id, text='Пост успешно отправлен', reply_markup=ReplyKeyboardRemove())
    for member in db.select_all_users():
        await bot.send_message(chat_id=member[0], text=post_text,
                               reply_markup=ReplyKeyboardRemove(), disable_web_page_preview=True)
    try:
        db1.add_user(id=name_post, name=body_post)
    except sqlite3.IntegrityError as err:
        print(err)
    await state.finish()


@dp.message_handler(state=Post.choise, text='Да')
async def new_post(message: types.Message, state: FSMContext):
    await bot.send_message(chat_id=message.chat.id, text='Превью ссылок будут отображаться',
                           reply_markup=view)
    await message.answer('Выберете нужный вариант')
    await Post.photo_no_preview_yes.set()


@dp.message_handler(state=Post.photo_no_preview_yes, text='Предпросмотр')
async def answer(message: types.Message, state: FSMContext):
    data = await state.get_data()
    name_post = data.get('post_name')
    body_post = data.get('post_body')
    post_text = name_post + '\n' + body_post
    await message.answer(post_text)


@dp.message_handler(state=Post.photo_no_preview_yes, text='Отправить')
async def answer(message: types.Message, state: FSMContext):
    data = await state.get_data()
    name_post = data.get('post_name')
    body_post = data.get('post_body')
    post_text = name_post + '\n' + body_post
    await bot.send_message(message.chat.id, text='Пост успешно отправлен', reply_markup=ReplyKeyboardRemove())
    for member in db.select_all_users():
        await bot.send_message(chat_id=member[0], text=post_text,
                               reply_markup=ReplyKeyboardRemove())
    try:
        db1.add_user(id=name_post, name=body_post)
    except sqlite3.IntegrityError as err:
        print(err)

    await state.finish()



