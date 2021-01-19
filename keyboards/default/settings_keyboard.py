from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from loader import _


def get_settings_keyboard(lang):
    settings_keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=_("🔄 Change Language", locale=lang)),
            ],
            [
                KeyboardButton(text=_("✍️ Edit Name", locale=lang))
            ],
            [
                KeyboardButton(text=_("✍️ Edit Phone Number", locale=lang))
            ],
            [
                KeyboardButton(text=_("🔙 Back", locale=lang))
            ]
        ],
        resize_keyboard=True
    )

    return settings_keyboard
