from aiogram.utils.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from utils.db_api.db_commands import get_categories, count_items, get_subcategories, get_items

menu_cd = CallbackData("show_menu", "level", "category", "subcategory", "item_id")
buy_item = CallbackData("buy", "item_id")


def make_callback_data(level, category="0", subcategory="0", item_id="0"):
    return menu_cd.new(level=level, category=category,
                       subcategory=subcategory, item_id=item_id)


async def categories_keyboard():
    CURRENT_LEVEL = 0
    markup = InlineKeyboardMarkup()

    categories = await get_categories()

    for category in categories:
        number_if_items = await count_items(category.category_code)
        button_text = f"{category.category_name} ({number_if_items} p.)"
        callback_data = make_callback_data(level=CURRENT_LEVEL + 1,
                                           category=category.category_code)

        markup.insert(
            InlineKeyboardButton(text=button_text, callback_data=callback_data)
        )

    return markup


async def subcategories_keyboard(category):
    CURRENT_LEVEL = 1
    markup = InlineKeyboardMarkup()

    subcategories = await get_subcategories(category)

    for subcategory in subcategories:
        number_if_items = await count_items(category.category, subcategory.subcategory)
        button_text = f"{subcategory.subcategory_name} ({number_if_items} p.)"
        callback_data = make_callback_data(level=CURRENT_LEVEL + 1,
                                           category=category,
                                           subcategory=subcategory.subcategory_code)

        markup.insert(
            InlineKeyboardButton(text=button_text, callback_data=callback_data)
        )

    markup.row(
        InlineKeyboardButton(
            text="Back",
            callback_data=make_callback_data(level=CURRENT_LEVEL - 1))
    )

    return markup


async def items_keyboard(category, subcategory):
    CURRENT_LEVEL = 2
    markup = InlineKeyboardMarkup(row_width=1)

    items = await get_items(category, subcategory)

    for item in items:
        button_text = f"{item.name} - {item.price} UZS"
        callback_data = make_callback_data(level=CURRENT_LEVEL+1,
                                           category=category,
                                           subcategory=subcategory,
                                           item_id=item.id)

        markup.insert(
            InlineKeyboardButton(text=button_text, callback_data=callback_data)
        )

    markup.row(
        InlineKeyboardButton(
            text="Back",
            callback_data=make_callback_data(level=CURRENT_LEVEL - 1,
                                             category=category))
    )

    return markup


def item_keyboard(category, subcategory, item_id):
    CURRENT_LEVEL = 3
    markup = InlineKeyboardMarkup()

    markup.row(
        InlineKeyboardButton(text="Buy", callback_data=buy_item.new(item_id=item_id))
    )

    markup.row(
        InlineKeyboardButton(text="Back", callback_data=make_callback_data(level=CURRENT_LEVEL - 1,
                                                                           category=category,
                                                                           subcategory=subcategory))
    )

    return markup



