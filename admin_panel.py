import re
from asyncio import sleep

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardRemove

from data.config import admins
from keyboards.default.choose_category import choose_category_keyboard
from keyboards.inline import sizes_keyboard
from keyboards.inline.callback_datas import size_callback, finish_callback
from loader import dp, _, bot
from states.states import NewItem, Mailing
from utils.db_api.models import Item, User


name_to_code = {
    '👚 Рубашки/Блузки': 'shirts',
    '👗 Платья': 'dresses',
    '🥻 Сарафаны': 'sundresses',
    '👖 Брюки': 'trousers',
    '🩳 Юбки': 'skirts',
    '📦 Другое': 'other'
}

name_to_name = {
    '👚 Рубашки/Блузки': '👚 Shirts/Blouses',
    '👗 Платья': '👗 Dresses',
    '🥻 Сарафаны': '🥻 Sundresses',
    '👖 Брюки': '👖 Trousers',
    '🩳 Юбки': '🩳 Skirts',
    '📦 Другое': '📦 Other'
}


@dp.message_handler(user_id=admins, commands=["cancel"], state=NewItem)
async def cancel(message: types.Message, state: FSMContext):
    await message.answer("Вы отменили создание товара!")
    await state.reset_state()


"""
Handlers for Adding New Item
"""


@dp.message_handler(user_id=admins, commands=["add_item"], state='*')
async def add_item(message: types.Message):
    await message.answer("Введите название товара или отмените создание товара, нажав /cancel")
    await NewItem.Name.set()


@dp.message_handler(user_id=admins, state=NewItem.Name)
async def enter_item_name(message: types.Message, state: FSMContext):
    name = message.text
    item = Item()
    item.name = name
    await message.answer("<b>Название:</b> {name}"
                         "\n\nВыберите категорию товара или отмените создание товара, нажав /cancel".format(name=name),
                         reply_markup=choose_category_keyboard)
    await NewItem.Category.set()
    await state.update_data(item=item)


@dp.message_handler(user_id=admins, state=NewItem.Category)
async def enter_category(message: types.Message, state: FSMContext):
    category = message.text
    data = await state.get_data()
    item: Item = data.get("item")
    item.category_name = name_to_name[category]
    item.category_code = name_to_code[category]
    await message.answer("<b>Название:</b> {name}"
                         "\n<b>Категория:</b> {category}"
                         "\n\nПришлите мне фотографию товара или отмените создание товара, нажав /cancel".format(name=item.name, category=category),
                         reply_markup=ReplyKeyboardRemove())
    await NewItem.Photo.set()
    await state.update_data(item=item)


@dp.message_handler(user_id=admins, state=NewItem.Photo, content_types=types.ContentType.PHOTO)
async def add_photo(message: types.Message, state: FSMContext):
    photo = message.photo[-1].file_id
    data = await state.get_data()
    item: Item = data.get("item")
    item.photo = photo
    await message.answer_photo(
        photo=photo,
        caption="<b>Название:</b> {name}"
                "\n<b>Категория:</b> {category}"
                "\n\nВыберите размеры товара в наличии или отмените создание товара, нажав /cancel".format(name=item.name,
                                                                                                           category=item.category_name),
        reply_markup=sizes_keyboard
    )
    await NewItem.Sizes.set()
    await state.update_data(item=item)


@dp.callback_query_handler(size_callback.filter(chosen_size=['xs', 's', 'm', 'l', 'xl', 'xxl']), user_id=admins, state=NewItem.Sizes)
async def add_sizes(call: types.CallbackQuery, state: FSMContext, callback_data: dict):
    size = callback_data['chosen_size'].upper()

    data = await state.get_data()
    item: Item = data.get("item")
    chosen_sizes = data.get("chosen_sizes")

    if not chosen_sizes:
        chosen_sizes = [size]
    else:
        if size not in chosen_sizes:
            chosen_sizes.append(size)
        else:
            chosen_sizes.remove(size)

    if not chosen_sizes:
        item.available_sizes = 'Не выбрано'
    else:
        item.available_sizes = ", ".join(chosen_sizes)

    await state.update_data(chosen_sizes=chosen_sizes)

    await bot.edit_message_caption(
        call.from_user.id,
        call.message.message_id,
        call.inline_message_id,
        "<b>Название:</b> {name}"
        "\n<b>Категория:</b> {category}"
        "\n<b>Размеры:</b> {sizes}".format(name=item.name, category=item.category_name, sizes=item.available_sizes),
        reply_markup=sizes_keyboard
    )
    await state.update_data(item=item)


@dp.callback_query_handler(finish_callback.filter(finish='true'), user_id=admins, state=NewItem.Sizes)
async def finish_size(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    chosen_sizes = data.get("chosen_sizes")
    if not chosen_sizes:
        await call.answer(text="Размеры не выбраны", show_alert=True)
        return

    await state.update_data(chosen_sizes=None)

    item: Item = data.get("item")
    await bot.delete_message(call.from_user.id, call.message.message_id)
    await bot.send_message(call.from_user.id,
                           "<b>Название:</b> {name}"
                           "\n<b>Категория:</b> {category}"
                           "\n<b>Размеры: </b> {sizes}"
                           "\n\nВведите стоимость товара или отмените создание товара, нажав /cancel"
                           .format(name=item.name, category=item.category_name, sizes=item.available_sizes)
                           )

    await NewItem.Price.set()


@dp.message_handler(user_id=admins, state=NewItem.Price)
async def enter_price(message: types.Message, state: FSMContext):
    data = await state.get_data()
    item: Item = data.get("item")
    price = message.text

    if re.match("^[0-9]*$", price):
        price = price[:-3] + " " + price[-3:]
    else:
        await message.answer("Неверное значение, введите заново!")
        return

    item.price = price

    markup = types.InlineKeyboardMarkup(
        inline_keyboard=[
            [types.InlineKeyboardButton(
                text="Да",
                callback_data="confirm")],
            [types.InlineKeyboardButton(
                text="Ввести заново",
                callback_data="change")]
        ]
    )

    await message.answer(
        "<b>Стоимость:</b> {price} сум\n"
        "Потверждаете? Нажмите /cancel чтобы отменить".format(price=price),
        reply_markup=markup
    )

    await state.update_data(item=item)

    await NewItem.Confirm.set()


@dp.callback_query_handler(user_id=admins,
                           text_contains="change",
                           state=NewItem.Confirm)
async def change_price(call: types.CallbackQuery):
    await call.message.edit_reply_markup()
    await call.message.answer("Введите стоимость заново")
    await NewItem.Price.set()


@dp.callback_query_handler(user_id=admins,
                           text_contains="confirm",
                           state=NewItem.Confirm)
async def confirm(call: types.CallbackQuery, state: FSMContext):
    await call.message.edit_reply_markup()
    data = await state.get_data()
    item: Item = data.get("item")
    await item.create()
    await call.message.answer("Товар был успешно создан! Создать еще - /add_item")
    await state.reset_state()


"""
Handlers for Mailing
"""


@dp.message_handler(user_id=admins, commands=["mail"])
async def mailing(message: types.Message):
    await message.answer("Введите текст рассылки")
    await Mailing.Text.set()


@dp.message_handler(user_id=admins, state=Mailing.Text)
async def enter_text(message: types.Message, state: FSMContext):
    text = message.text
    await state.update_data(text=text)

    markup = types.InlineKeyboardMarkup(
        inline_keyboard=[
            [types.InlineKeyboardButton(
                text="English",
                callback_data="en")],
            [types.InlineKeyboardButton(
                text="Русский",
                callback_data="ru")],
            [types.InlineKeyboardButton(
                text="O'zbek tili",
                callback_data="uz")]
        ]
    )

    await message.answer("Выберите язык рассылки\n\n"
                         "<b>Текст:</b>\n"
                         "{text}".format(text=text),
                         reply_markup=markup)

    await Mailing.Language.set()


@dp.callback_query_handler(user_id=admins, state=Mailing.Language)
async def enter_lang(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    text = data.get("text")
    await state.reset_state()
    await call.message.edit_reply_markup()
    users = await User.query.where(User.language == call.data).gino.all()
    for user in users:
        try:
            await bot.send_message(chat_id=user.user_id,
                                   text=text)
            await sleep(0.3)
        except Exception:
            pass
    await call.message.answer("Рассылка успешно завершена!")
