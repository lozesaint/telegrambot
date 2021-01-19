from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from loader import _


def get_location_keyboard(lang):
    location_keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=_("📍 Share Current Location", locale=lang),
                               request_location=True)
            ],
            [
                KeyboardButton(text=_("✖️ Cancel", locale=lang))
            ]
        ],
        resize_keyboard=True,
        one_time_keyboard=True,
    )

    return location_keyboard