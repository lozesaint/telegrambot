from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

language_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="🇺🇸 English")
        ],
        [
            KeyboardButton(text="🇷🇺 Русский")
        ],
        [
            KeyboardButton(text="🇺🇿 O'zbek tili")
        ],
    ],
    resize_keyboard=True
)
