from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandHelp
from aiogram.types import ReplyKeyboardRemove

from loader import dp
from utils.misc import rate_limit


@rate_limit(5, 'help')
@dp.message_handler(CommandHelp())
async def bot_help(message: types.Message):
    text = [
        "Welcome to the Help option:\n",
        "/start - Start the <b>MustHave Official's</b> Bot",
        "/help - Get the commands list",
        "/menu - Get the Main Menu",
    ]
    await message.answer('\n'.join(text), reply_markup=ReplyKeyboardRemove())
