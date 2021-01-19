from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from loader import _
from keyboards.inline.callback_datas import pay_method_cd


def get_payment_keyboard(lang):
    payment_keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=_("💵 Cash", locale=lang),
                                     callback_data=pay_method_cd.new(method="cash"))
            ],
            [
                InlineKeyboardButton(text="💳 Click",
                                     callback_data=pay_method_cd.new(method="click"))
            ],
            [
                InlineKeyboardButton(text="💳 PayMe",
                                     callback_data=pay_method_cd.new(method="payme"))
            ],
            [
                InlineKeyboardButton(text="💳 Apelsin",
                                     callback_data=pay_method_cd.new(method="apelsin"))
            ]
        ]
    )

    return payment_keyboard
