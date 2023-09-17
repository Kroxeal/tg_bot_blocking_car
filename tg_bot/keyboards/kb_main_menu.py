from aiogram import types

kb_main_menu = [
    [
    types.KeyboardButton(text='Зарегистрироваться'),
    types.KeyboardButton(text='Зарегестрировать машину'),
    ],
    [
    types.KeyboardButton(text='Я подпер машину'),
    types.KeyboardButton(text='Мою машину подперли'),
    ],
]

keyboard_menu = types.ReplyKeyboardMarkup(
    keyboard=kb_main_menu,
    resize_keyboard=True,
    input_field_placeholder="Сделайте выбор "
)
