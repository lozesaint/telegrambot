from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from loader import _


def get_language_keyboard(lang):
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
            [
                KeyboardButton(text=_("🔙 Back", locale=lang))
            ]
        ],
        resize_keyboard=True
    )

    return language_keyboard
