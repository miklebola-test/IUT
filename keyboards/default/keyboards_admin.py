from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ForceReply

menu = ReplyKeyboardMarkup(
    [
        [
            KeyboardButton(text='Написать новый пост')
        ],
        [
            KeyboardButton(text='Посмотреть отправленные ранее посты')
        ]
    ],
    resize_keyboard=True
)

yes_no = ReplyKeyboardMarkup(
    [
        [
            KeyboardButton(text='Да'),
            KeyboardButton(text='Нет')
        ]
    ],
    resize_keyboard=True
)

view = ReplyKeyboardMarkup(
    [
        [
            KeyboardButton(text='Предпросмотр'),
            KeyboardButton(text='Отправить')
        ]
    ],
    resize_keyboard=True
)

back = ReplyKeyboardMarkup(
    [
        [
            KeyboardButton(text='Вернуться назад')
        ]
    ],
    resize_keyboard=True
)
