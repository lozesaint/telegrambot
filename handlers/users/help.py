from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandHelp
from aiogram.types import ReplyKeyboardRemove

from data.config import admins
from loader import dp
from utils.misc import rate_limit


@rate_limit(5, 'help')
@dp.message_handler(CommandHelp())
async def bot_help(message: types.Message):
    chat_id = message.from_user.id

    text = [
        "Welcome to the Help option:\n",
        "/start - Start the <b>MustHave Official's</b> Bot",
        "/menu - Get the Main Menu",
    ]

    for admin in admins:
        if chat_id == int(admin):
            text.extend(["\n\n",
                         "------ Админ Панель -------\n",
                         "/add_item - Добавить новый товар\n",
                         "/mail - Сделать рассылку"])

    await message.answer('\n'.join(text), reply_markup=ReplyKeyboardRemove())

