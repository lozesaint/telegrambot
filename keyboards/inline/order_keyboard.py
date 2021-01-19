from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from keyboards.inline.callback_datas import order_phase_cd


def get_order_keyboard_phase_1(order_id, user_id):
    order_keyboard_phase_1 = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Статус: Новое",
                                     callback_data="none"),

            ],
            [
                InlineKeyboardButton(text="✅ Потвердить",
                                     callback_data=f"confirm_{order_id}_{user_id}"),
                InlineKeyboardButton(text="❎ Отменить",
                                     callback_data=f"cancel_{order_id}_{user_id}")
            ]
        ]
    )
    return order_keyboard_phase_1


def get_order_keyboard_phase_2(order_id, user_id):
    order_keyboard_phase_2 = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Статус: Ожидание Оплаты",
                                     callback_data="none"),

            ],
            [
                InlineKeyboardButton(text="✅ Оплата Завершена",
                                     callback_data=f'success_{order_id}_{user_id}'),
            ]
        ]
    )
    return order_keyboard_phase_2


order_keyboard_phase_3 = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Статус: Оплачено",
                                 callback_data="none"),

        ]
    ]
)

order_keyboard_phase_0 = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Статус: Отменено",
                                 callback_data="none"),

        ]
    ]
)

