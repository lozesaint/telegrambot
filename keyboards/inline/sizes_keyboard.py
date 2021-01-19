from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from .callback_datas import size_callback, finish_callback

sizes_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='XS',
                                 callback_data=size_callback.new(chosen_size='xs')),
            InlineKeyboardButton(text='S',
                                 callback_data=size_callback.new(chosen_size='s')),
            InlineKeyboardButton(text='M',
                                 callback_data=size_callback.new(chosen_size='m')),
        ],
        [
            InlineKeyboardButton(text='L',
                                 callback_data=size_callback.new(chosen_size='l')),
            InlineKeyboardButton(text='XL',
                                 callback_data=size_callback.new(chosen_size='xl')),
            InlineKeyboardButton(text='XXL',
                                 callback_data=size_callback.new(chosen_size='xxl')),
        ],
        [
            InlineKeyboardButton(text='Это всё',
                                 callback_data=finish_callback.new(finish='true'))
        ]
    ]
)