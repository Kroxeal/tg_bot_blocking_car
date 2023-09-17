from aiogram import types


kb_yes_no = [
    [
    types.KeyboardButton(text='Да'),
    types.KeyboardButton(text='Нет'),
    ],
]

keyboard_is_blocked = types.ReplyKeyboardMarkup(
    keyboard=kb_yes_no,
    resize_keyboard=True,
    input_field_placeholder="Выберете Да или Нет "
)
