from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

choose_category_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="👚 Рубашки/Блузки"),
            KeyboardButton(text="👗 Платья"),
        ],
        [
            KeyboardButton(text="🥻 Сарафаны"),
            KeyboardButton(text="👖 Брюки"),
        ],
        [
            KeyboardButton(text="🩳 Юбки"),
            KeyboardButton(text="📦 Другое"),
        ]
    ],
    resize_keyboard=True
)