
from typing import Union

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.types import Message, ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, CallbackQuery

from data.config import admins
from keyboards.inline import get_categories_keyboard
from utils.db_api import db_commands

from keyboards.default import get_language_keyboard, get_settings_keyboard, get_contact_keyboard
from keyboards.default.feedback_keyboard import get_feedback_keyboard
from keyboards.default.about_keyboard import get_about_keyboard
from keyboards.default.menu_keyboards import get_main_menu_keyboard
from loader import dp, _, bot
from states.states import Feedback, Settings, Menu

db = db_commands.DBCommands()

category_associations = {
    '👚 Shirts/Blouses': 'shirts',
    '👗 Dresses': 'dresses',
    '🥻 Sundresses': 'sundresses',
    '👖 Trousers': 'trousers',
    '🩳 Skirts': 'skirts',
}


@dp.message_handler(text=["🔙 Back", "🔙 Назад", "🔙 Ortga"], state=[Menu.Category, Menu.About, Feedback, Menu.Settings])
async def go_back(message: Message):
    await show_menu(message)


@dp.message_handler(text=["🔙 Back", "🔙 Назад", "🔙 Ortga"], state=[Settings.InputtingPhone, Settings.InputtingName, Settings.ChangeLanguage])
async def go_back(message: Message):
    await show_settings(message)


@dp.message_handler(Command("menu"), state="*")
async def show_menu(message: Union[Message, CallbackQuery]):
    user = await db.get_user(message.from_user.id)

    print("lang=", user.language)

    if isinstance(message, Message):
        await message.answer(_("Main Menu"), reply_markup=get_main_menu_keyboard(user.language))
    elif isinstance(message, CallbackQuery):
        await message.message.answer(_("Main Menu"), reply_markup=get_main_menu_keyboard(user.language))

    await Menu.Main_Menu.set()


"""
First level Buttons
"""


@dp.message_handler(text=['🛍 Shop', '🛍 Магазин', '🛍 Magazin'], state=Menu.Main_Menu)
async def show_shop(message: Message, state: FSMContext):
    user = await db.get_user(message.from_user.id)

    await message.answer(text=_("Great! Where do we start?"), reply_markup=ReplyKeyboardRemove())
    await state.update_data(message_ids=[])
    await message.answer(text=_("Categories Menu"), reply_markup=get_categories_keyboard(user.language))

    await Menu.Category.set()


@dp.message_handler(text=["❗ Help", "❗ Помощь", "❗ Yordam"], state=Menu.Main_Menu)
async def show_help(message: types.Message):
    chat_id = message.from_user.id

    text = [
        _("Available commands:\n"),
        _("/start - Start the <b>MustHave Official's</b> Bot"),
        _("/menu - Main Menu"),
    ]

    for admin in admins:
        if chat_id == int(admin):
            text.extend(["\n\n",
                         "----------------- <b>Админ Панель</b> -----------------\n",
                         "/add_item - Добавить новый товар\n",
                         "/mail - Сделать рассылку"])

    await message.answer('\n'.join(text))


@dp.message_handler(state=Menu.Main_Menu, text=["ℹ About", "ℹ О Нас", "ℹ Biz haqimizda"])
async def show_about(message: Message):
    user = await db.get_user(message.from_user.id)

    await message.answer(_("What do you want to know about us?"), reply_markup=get_about_keyboard(user.language))

    await Menu.About.set()


@dp.message_handler(text=["🗣 Feedback", "🗣 Обратная связь", "🗣 Munosabat bildirish"], state=Menu.Main_Menu)
async def show_feedback(message: Message):
    user = await db.get_user(message.from_user.id)

    await message.answer(_("We will be thankful if you will help our services improve!\n"
                           "Leave your feedback or rate us on a 5-point scale!"), reply_markup=get_feedback_keyboard(user.language))

    await Feedback.Answer.set()


@dp.message_handler(text=["⚙ Settings", "⚙ Настройки", "⚙ Sozlamalar"], state=Menu.Main_Menu)
async def show_settings(message: Message):
    user = await db.get_user(message.from_user.id)

    await message.answer(_("Settings Menu:", locale=user.language), reply_markup=get_settings_keyboard(user.language))

    await Menu.Settings.set()


"""
Second level Buttons
"""


@dp.message_handler(state=Menu.About, text=["📍 Shop's Location", "📍 Локация Магазина", "📍 Magazinimiz joylashuvi"])
async def show_location(message: Message):
    await message.answer(_("Location information:\n\n"
                           "<b>📍 Address:</b> Tashkent, Mirabad District, Avliyoota Street, 2\n\n"
                           "<b>🗺 Reference Point:</b> Mirabad (Hospital) Bazaar, near to \"Мисс Камилла\" wedding salon. Store \"Molly\"\n\n"
                           "<b>🕓 We work 7 days a week </b>\n\n"
                           "<b>💸 Payment Methods:</b>\n"
                           "1. Cash\n"
                           "2. Click\n"
                           "3. PayMe\n"
                           "4. Apelsin"
                           ))
    await bot.send_location(chat_id=message.from_user.id,
                            latitude=41.29237577846323,
                            longitude=69.27519142336128)


@dp.message_handler(state=Menu.About, text=["📱 Contacts", "📱 Контакты", "📱 Bog'lanish ma'lumotlari"])
async def show_contacts(message: Message):
    text = _("Contact information:\n\n" 
             "📞 Phone Number #1\n" 
             "+998(99) 842-67-09\n\n" 
             "📞 Phone Number #2\n" 
             "+998(97) 768-68-49\n\n" 
             "<b>📲 Telegram:</b> \n@musthaveuzb\n\n" 
             "<b>📲 Instagram:</b> \nhttps://www.instagram.com/musthave.uz/")
    await message.answer(text)


@dp.message_handler(state=Feedback.Answer)
async def get_feedback(message: Message):
    feedback = message.text
    await db.set_feedback(feedback)
    await message.answer(_("Thank you for your response!"))

    await show_menu(message)


@dp.message_handler(state=Menu.Settings, text=["✍️ Edit Name", "✍️ Изменить Имя", "✍️ Ismni o'zgartirish"])
async def edit_name(message: Message):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.insert(
        KeyboardButton(text=_("🔙 Back"))
    )

    await message.answer(_("Enter your new name"), reply_markup=markup)

    await Settings.InputtingName.set()


@dp.message_handler(state=Settings.InputtingName)
async def inputting_name(message: Message):
    name = message.text
    await db.set_name(name)
    await message.answer(_("Your name has been changed!"))

    await show_settings(message)


@dp.message_handler(state=Menu.Settings, text=["✍️ Edit Phone Number", "✍️ Изменить Номер Телефона", "✍️ Telefon raqamini o'zgartirish"])
async def edit_number(message: Message):
    user = await db.get_user(message.from_user.id)

    await message.answer(_("Enter your new phone number"), reply_markup=get_contact_keyboard(user.language))

    await Settings.InputtingPhone.set()


@dp.message_handler(state=Settings.InputtingPhone, content_types=types.ContentTypes.CONTACT)
async def inputting_number(message: Message):
    number = message.contact.phone_number
    await db.set_phone_number(number)
    await message.answer(_("Your phone number has been changed!"))

    await show_settings(message)


@dp.message_handler(state=Settings.InputtingPhone, regexp="^[+]*[(]{0,1}[0-9]{1,4}[)]{0,1}[-\s\./0-9]*$")
async def inputting_number(message: Message):
    number = message.text

    await db.set_phone_number(number)
    await message.answer(_("Your phone number has been changed!"))

    await show_settings(message)


@dp.message_handler(text=["🔄 Change Language", "🔄 Сменить Язык", "🔄 Tilni o'zgartirish"], state=Menu.Settings)
async def change_language(message: Message):
    user = await db.get_user(message.from_user.id)

    await message.answer(_("Choose the language"), reply_markup=get_language_keyboard(user.language))

    await Settings.ChangeLanguage.set()


@dp.message_handler(state=Settings.ChangeLanguage, text_contains="English")
async def choosing_en(message: Message):
    await db.set_language("en")
    await message.answer(_("Great! Your language has been changed", locale="en"))

    await show_settings(message)


@dp.message_handler(state=Settings.ChangeLanguage, text_contains="Русский")
async def choosing_ru(message: Message):
    await db.set_language("ru")
    await message.answer(_("Great! Your language has been changed", locale="ru"))

    await show_settings(message)


@dp.message_handler(state=Settings.ChangeLanguage, text_contains="O'zbek")
async def choosing_uz(message: Message):
    await db.set_language("uz")
    await message.answer(_("Great! Your language has been changed", locale="uz"))

    await show_settings(message)
