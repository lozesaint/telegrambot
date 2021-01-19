from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from loader import _
from keyboards.inline.callback_datas import back_to_menu


def get_categories_keyboard(lang):
    categories_keyboard = InlineKeyboardMarkup(row_width=4,
                                               inline_keyboard=[
                                                   [
                                                       InlineKeyboardButton(
                                                           text=_("🏪 All products", locale=lang),
                                                           switch_inline_query_current_chat="🏪"
                                                       ),
                                                       InlineKeyboardButton(
                                                           text=_("🛒 Cart", locale=lang),
                                                           callback_data="show_cart"
                                                       )
                                                   ],
                                                   [
                                                       InlineKeyboardButton(
                                                           text=_("👚 Shirts/Blouses", locale=lang),
                                                           switch_inline_query_current_chat="👚"
                                                       ),
                                                       InlineKeyboardButton(
                                                           text=_("👗 Dresses", locale=lang),
                                                           switch_inline_query_current_chat="👗"
                                                       )
                                                   ],
                                                   [
                                                       InlineKeyboardButton(
                                                           text=_("🥻 Sundresses", locale=lang),
                                                           switch_inline_query_current_chat="🥻"
                                                       ),
                                                       InlineKeyboardButton(
                                                           text=_("👖 Trousers", locale=lang),
                                                           switch_inline_query_current_chat="👖"
                                                       )
                                                   ],
                                                   [
                                                       InlineKeyboardButton(
                                                           text=_("🩳 Skirts", locale=lang),
                                                           switch_inline_query_current_chat="🩳"
                                                       ),
                                                       InlineKeyboardButton(
                                                           text=_("📦 Other", locale=lang),
                                                           switch_inline_query_current_chat="📦"
                                                       )
                                                   ],
                                                   [
                                                       InlineKeyboardButton(
                                                           text=_("🔙 Back", locale=lang),
                                                           callback_data=back_to_menu.new(action="back_to_main")
                                                       ),
                                                   ]
                                               ])

    return categories_keyboard
