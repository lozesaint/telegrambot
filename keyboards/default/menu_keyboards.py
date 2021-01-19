from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from loader import _


def get_main_menu_keyboard(lang):

    main_menu_keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=_("🛍 Shop", locale=lang))
            ],
            [
                KeyboardButton(text=_("🗣 Feedback", locale=lang)),
                KeyboardButton(text=_("ℹ About", locale=lang)),
            ],
            [
                KeyboardButton(text=_("❗ Help", locale=lang)),
                KeyboardButton(text=_("⚙ Settings", locale=lang)),
            ],

        ],
        resize_keyboard=True
    )

    return main_menu_keyboard


