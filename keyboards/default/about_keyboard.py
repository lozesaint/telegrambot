from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from loader import _


def get_about_keyboard(lang):
    about_keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=_("📍 Shop's Location", locale=lang))
            ],
            [
                KeyboardButton(text=_("📱 Contacts", locale=lang)),
            ],
            [
                KeyboardButton(text=_("🔙 Back", locale=lang))
            ]
        ],
        resize_keyboard=True
    )

    return about_keyboard
