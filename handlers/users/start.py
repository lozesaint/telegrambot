import re

from geopy.geocoders import Nominatim

from aiogram import types
from aiogram.dispatcher.storage import FSMContext
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.types import CallbackQuery, ReplyKeyboardRemove

from keyboards.default import location_keyboard, contact_keyboard, menu_keyboard, catalog_keyboard, language_keyboard
from loader import dp
from states import QuestionsOnStart
from utils.misc import rate_limit

from utils.db_api import quick_commands as commands


@rate_limit(3)
@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    await message.answer("Welcome to <b>MustHave Official's</b> Bot!\n\n"
                         "Choose your preferred language",
                         reply_markup=language_keyboard)

    await QuestionsOnStart.users_pref_language.set()


@dp.message_handler(state=QuestionsOnStart.users_pref_language, text_contains="En")
async def choosing_en(message: types.Message, state: FSMContext):
    await state.update_data(users_pref_language="en")
    await message.answer(text="You chose English", reply_markup=ReplyKeyboardRemove())
    data = await state.get_data()
    lang = data.get("users_pref_language")

    await commands.add_user(id=message.from_user.id,
                            name=message.from_user.full_name,
                            lang=lang)

    await state.reset_state(with_data=False)


@dp.message_handler(state=QuestionsOnStart.users_pref_language, text_contains="Ру")
async def choosing_ru(message: types.Message, state: FSMContext):
    await state.update_data(users_pref_language="ru")
    await message.answer(text="You chose Russian", reply_markup=ReplyKeyboardRemove())
    data = await state.get_data()
    lang = data.get("users_pref_language")

    await commands.add_user(id=message.from_user.id,
                            name=message.from_user.full_name,
                            lang=lang)

    await state.reset_state(with_data=False)


@dp.message_handler(state=QuestionsOnStart.users_pref_language, text_contains="O'z")
async def choosing_uz(message: types.Message, state: FSMContext):
    await state.update_data(users_pref_language="uz")
    await message.answer(text="You chose Uzbek", reply_markup=ReplyKeyboardRemove())
    data = await state.get_data()
    lang = data.get("users_pref_language")

    await commands.add_user(id=message.from_user.id,
                            name=message.from_user.full_name,
                            lang=lang)

    await state.reset_state(with_data=False)


# @dp.message_handler(text_contains="Catalog")
# async def show_catalog(message: types.Message):
#     await message.answer("Let us get started", reply_markup=catalog_keyboard)
#
#     @dp.message_handler(text_contains="Trending")
#     async def show_catalog_trending(message: types.Message):
#         await message.answer("You chose Catalog -> Trending")
#
#     @dp.message_handler(text_contains="Tops")
#     async def show_catalog_tops(message: types.Message):
#         await message.answer("You chose Catalog -> Tops")
#
#     @dp.message_handler(text_contains="Bottoms")
#     async def show_catalog_bottoms(message: types.Message):
#         await message.answer("You chose Catalog -> Bottoms")
#
#     @dp.message_handler(text_contains="Dresses")
#     async def show_catalog_dresses(message: types.Message):
#         await message.answer("You chose Catalog -> Dresses")
#
#     @dp.message_handler(text_contains="Shoes")
#     async def show_catalog_shoes(message: types.Message):
#         await message.answer("You chose Catalog -> Shoes")
#
#     @dp.message_handler(text_contains="Outwear")
#     async def show_catalog_outwear(message: types.Message):
#         await message.answer("You chose Catalog -> Outwear")
#
#     @dp.message_handler(text_contains="Brand")
#     async def show_catalog_brand(message: types.Message):
#         await message.answer("You chose Catalog -> Brands")
#
#
# @dp.message_handler(text_contains="Feedback")
# async def show_feedback(message: types.Message):
#     await message.answer("You chose Feedback")
#
#
# @dp.message_handler(text_contains="About")
# async def show_about(message: types.Message):
#     await message.answer("You chose About")
#
#
# @dp.message_handler(text_contains="Cart")
# async def show_cart(message: types.Message):
#     await message.answer("You chose Cart")
#
#
# @dp.message_handler(text_contains="Settings")
# async def show_settings(message: types.Message):
#     await message.answer("You chose Settings")



#     await message.answer("Welcome to <b>MustHave Official's</b> Bot!\n\n"
#                          "Please, enter your full name: ",
#                          reply_markup=ReplyKeyboardRemove())
#
#     await QuestionsOnStart.users_name.set()
#
#
# @dp.message_handler(state=QuestionsOnStart.users_name)
# async def get_users_name(message: types.Message, state: FSMContext):
#     users_name = message.text
#     if not re.match('^[ЁёА-яA-Za-z\s]+$', users_name):
#         await message.answer(f"Invalid Name {message.text}. Try Again.")
#         await QuestionsOnStart.users_name.set()
#         return
#
#     await state.update_data(users_name=users_name)
#
#     await message.answer("Send me your phone number", reply_markup=contact_keyboard)
#
#     await QuestionsOnStart.users_phone_number.set()
#
#
# @dp.message_handler(state=QuestionsOnStart.users_phone_number, content_types=types.ContentTypes.CONTACT | types.ContentTypes.TEXT)
# async def get_users_phone_number(message: types.Message, state: FSMContext):
#     users_phone_number = message.contact
#
#     # if not re.match('^[+]*[(]{0,1}[0-9]{1,4}[)]{0,1}[-\s\./0-9]*$', users_phone_number):
#     #     await message.answer(f"Invalid Phone Number {message.text}. Try Again.")
#     #     await QuestionsOnStart.users_phone_number.set()
#     #     return
#
#     await state.update_data(users_phone_number=users_phone_number.phone_number)
#
#     await message.answer("Send me your address: ", reply_markup=location_keyboard)
#
#     await QuestionsOnStart.users_address.set()
#
#
# @dp.message_handler(state=QuestionsOnStart.users_address, content_types=types.ContentTypes.LOCATION | types.ContentTypes.TEXT)
# async def get_users_address(message: types.Message, state: FSMContext):
#     if message.content_type == "LOCATION":
#         users_address = message.location
#         locator = Nominatim(user_agent="myGeocoder")
#         coordinates = [users_address.latitude, users_address.longitude]
#         location = locator.reverse(coordinates)
#
#         users_address_name = location.address
#     else:
#         users_address_name = message.text
#
#     await state.update_data(users_address=users_address_name)
#
#     await message.answer("Choose your preferred language: ", reply_markup=choice)
#
#     await QuestionsOnStart.users_pref_language.set()
#
#
# @dp.callback_query_handler(lang_callback.filter(chosen_lang="en"), state=QuestionsOnStart.users_pref_language)
# async def choosing_en(call: CallbackQuery, state: FSMContext):
#     await state.update_data(users_pref_language="en")
#     await call.answer(cache_time=60)
#
#     await show_personal_info(call.message, state)
#
#     await state.reset_state(with_data=False)
#
#
# @dp.callback_query_handler(lang_callback.filter(chosen_lang="ru"), state=QuestionsOnStart.users_pref_language)
# async def choosing_ru(call: CallbackQuery, state: FSMContext):
#     await state.update_data(users_pref_language="ru")
#     await call.answer(cache_time=60)
#
#     await show_personal_info(call.message, state)
#
#     await state.reset_state(with_data=False)
#
#
# @dp.callback_query_handler(lang_callback.filter(chosen_lang="uz"), state=QuestionsOnStart.users_pref_language)
# async def choosing_uz(call: CallbackQuery, state: FSMContext):
#     await state.update_data(users_pref_language="uz")
#     await call.answer(cache_time=60)
#
#     await show_personal_info(call.message, state)
#
#     await state.reset_state(with_data=False)
#
#
# async def show_personal_info(message, state):
#     data = await state.get_data()
#     users_name = data.get("users_name")
#     users_phone_number = data.get("users_phone_number")
#     users_address = data.get("users_address")
#     users_pref_language = data.get("users_pref_language")
#     await message.answer("Thank you for your answers!\n\n"
#                          f"<b>Your Name:</b> {users_name}\n\n"
#                          f"<b>Your Phone Number:</b> {users_phone_number}\n\n"
#                          f"<b>Your Address:</b> {users_address}\n\n"
#                          f"<b>Your Preferred Language:</b> {users_pref_language}")
