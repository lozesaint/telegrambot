from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import Command
from aiogram.utils.markdown import hcode

from loader import dp
from states import QuestionsOnStart

from utils.db_api import quick_commands as commands
from utils.misc import rate_limit


@rate_limit(3)
@dp.message_handler(Command("email"))
async def email_prompt(message: types.Message):
    await message.answer("Send me ur email")
    await QuestionsOnStart.users_email.set()


@dp.message_handler(state=QuestionsOnStart.users_email)
async def get_email(message: types.Message, state: FSMContext):
    email = message.text
    await commands.update_user_email(id=message.from_user.id, email=email)
    user = await commands.select_user(id=message.from_user.id)
    await message.answer("Data updated: \n" +
                         hcode(f"id={user.id}\n"
                               f"name={user.name}\n"
                               f"email={user.email}\n"))
    await state.finish()

