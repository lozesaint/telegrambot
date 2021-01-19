from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from loader import _
from utils.db_api import db_commands


async def get_size_keyboard(item_id):
    markup = InlineKeyboardMarkup()
    counter = 0

    item = await db_commands.get_item(item_id)

    for size in item.available_sizes.split(', '):
        button_text = size
        data = f"chosen_{size}"
        if counter % 2 == 0:
            markup.row(
                InlineKeyboardButton(text=button_text,
                                     callback_data=data)
            )
        else:
            markup.insert(
                InlineKeyboardButton(text=button_text,
                                     callback_data=data)
            )

        counter += 1

    markup.row(InlineKeyboardButton(text=_("🔙 Back"),
                                    callback_data=f"back_to_item_{item_id}"))

    return markup
