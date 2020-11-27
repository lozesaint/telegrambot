from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


catalog_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Trending (or New)")
        ],
        [
            KeyboardButton(text="Tops"),
            KeyboardButton(text="Bottoms"),
        ],
        [
            KeyboardButton(text="Dresses"),
            KeyboardButton(text="Shoes"),
        ],
        [
            KeyboardButton(text="Outwear"),
            KeyboardButton(text="Brands"),
        ],
    ],
    resize_keyboard=True
)