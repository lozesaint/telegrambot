from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from utils.db_api import db_commands
from loader import _
from keyboards.inline.callback_datas import cart_delete_cd, back_to_menu

db = db_commands.DBCommands()


def get_cart_keyboard(items):

    markup = InlineKeyboardMarkup()

    for index, item in enumerate(items, 1):
        markup.row(InlineKeyboardButton(text=f"❌ {item.name}",
                                        callback_data=cart_delete_cd.new(f"delete_{item.id}")))

    markup.row(InlineKeyboardButton(text=_("🚫 Clear cart"),
                                    callback_data="clear_cart"))
    markup.row(InlineKeyboardButton(text=_("🔙 Back"),
                                    callback_data=back_to_menu.new(action="back_to_category")))
    markup.row(InlineKeyboardButton(text=_("📤 Place Order"),
                                    callback_data="order"))

    return markup

