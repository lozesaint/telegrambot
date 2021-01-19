from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from loader import _


def get_feedback_keyboard(lang):
    feedback_keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="⭐️⭐️⭐️⭐️⭐️")
            ],
            [
                KeyboardButton(text="⭐️⭐️⭐️⭐️"),
            ],
            [
                KeyboardButton(text="⭐️⭐️⭐️"),
            ],
            [
                KeyboardButton(text="⭐️⭐️"),
            ],
            [
                KeyboardButton(text="⭐️"),
            ],
            [
                KeyboardButton(text=_("🔙 Back", locale=lang))
            ]
        ],
        resize_keyboard=True
    )

    return feedback_keyboard
