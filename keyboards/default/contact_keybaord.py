from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from loader import _


def get_contact_keyboard(lang):
    contact_keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=_("📱 Share Phone Number", locale=lang),
                               request_contact=True)
            ],
            [
                KeyboardButton(text=_("🔙 Back", locale=lang))
            ]
        ],
        resize_keyboard=True
    )

    return contact_keyboard
