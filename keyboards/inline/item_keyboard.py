from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from data.config import admins
from loader import _
from keyboards.inline.callback_datas import back_to_menu


def get_item_keyboard(category_name, item_id, user_id, active, lang):
    markup = InlineKeyboardMarkup()

    markup.row(InlineKeyboardButton(text=_("📥 Add to Cart", locale=lang),
                                    callback_data=f"add_item_{item_id}"))
    markup.row(InlineKeyboardButton(text=category_name[0],
                                    switch_inline_query_current_chat=category_name[0]))
    markup.row(InlineKeyboardButton(text=_("🔙 Back to Menu", locale=lang),
                                    callback_data=back_to_menu.new(action="back_to_category")))

    if str(user_id) in admins:
        if active:
            markup.row(InlineKeyboardButton(text="Товар активный: 🔒 Деактивировать",
                                            callback_data=f"disable_item_{item_id}"))
        else:
            markup.row(InlineKeyboardButton(text="Товар неактивный: 🔓 Активировать",
                                            callback_data=f"enable_item_{item_id}"))

    return markup
