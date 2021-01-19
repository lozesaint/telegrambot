from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from loader import _
from keyboards.inline.callback_datas import quantity_cd, back_to_menu


def get_quantity_keyboard(amount):
    markup = InlineKeyboardMarkup()

    markup.insert(
        InlineKeyboardButton(text="-",
                             callback_data=quantity_cd.new(action='minus', amount=amount))
    )
    markup.insert(
        InlineKeyboardButton(text=amount,
                             callback_data="none")
    )
    markup.insert(
        InlineKeyboardButton(text="+",
                             callback_data=quantity_cd.new(action='plus', amount=amount))
    )
    markup.row(
        InlineKeyboardButton(text=_("🔙 Back"),
                             callback_data=back_to_menu.new(action='back_to_size'))
    )
    markup.row(
        InlineKeyboardButton(text=_("📥 Add to Cart"),
                             callback_data=quantity_cd.new(action='add_to_cart', amount=amount))
    )

    return markup


