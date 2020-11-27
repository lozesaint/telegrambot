from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


menu_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="🛍 Catalog")
        ],
        [
            KeyboardButton(text="🗣 Feedback"),
            KeyboardButton(text="ℹ About"),
        ],
        [
            KeyboardButton(text="🔄 Change Language"),
        ]
    ],
    resize_keyboard=True
)