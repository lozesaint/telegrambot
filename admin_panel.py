from asyncio import sleep

from aiogram import types
from aiogram.dispatcher import FSMContext

from data.config import admins
from loader import dp, _, bot
from states.states import NewItem, Mailing
from utils.db_api.database import Item, User


@dp.message_handler(user_id=admins, commands=["cancel"], state=NewItem)
async def cancel(message: types.Message, state: FSMContext):
    await message.answer(_("You canceled your order"))
    await state.reset_state()


@dp.message_handler(user_id=admins, commands=["add_item"])
async def add_item(message: types.Message):
    await message.answer(_("Enter the item's name or press /cancel"))
    await NewItem.Name.set()


@dp.message_handler(user_id=admins, state=NewItem.Name)
async def enter_item_name(message: types.Message, state: FSMContext):
    name = message.text
    item = Item()
    item.name = name
    await message.answer(_("Name: {name}"
                           "\nSend me the photo or press /cancel").format(
        name=name
    ))
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
        caption=_("Name: {name}"
                  "\nSend me the price of the product or press /cancel").format(
            name=item.name
        )
    )
    await NewItem.Price.set()
    await state.update_data(item=item)


@dp.message_handler(user_id=admins, state=NewItem.Price)
async def enter_price(message: types.Message, state: FSMContext):
    data = await state.get_data()
    item: Item = data.get("item")
    try:
        price = int(message.text)
    except ValueError:
        await message.answer(_("Invalid input, enter a number"))
        return
    item.price = price

    markup = types.InlineKeyboardMarkup(
        inline_keyboard=[
            [types.InlineKeyboardButton(
                text=_("Yes"),
                callback_data="confirm")],
            [types.InlineKeyboardButton(
                text=_("Enter Again"),
                callback_data="change")]
        ]
    )

    await message.answer(
        _("Price: {price:,}\n"
          "Confirm? Press /cancel to cancel").format(price=price),
        reply_markup=markup
    )

    await state.update_data(item=item)

    await NewItem.Confirm.set()


@dp.callback_query_handler(user_id=admins,
                           text_contains="change",
                           state=NewItem.Confirm)
async def change_price(call: types.CallbackQuery):
    await call.message.edit_reply_markup()
    await call.message.answer(_("Enter the price again"))
    await NewItem.Price.set()


@dp.callback_query_handler(user_id=admins,
                           text_contains="comfirm",
                           state=NewItem.Confirm)
async def confirm(call: types.CallbackQuery, state: FSMContext):
    await call.message.edit_reply_markup()
    data = await state.get_data()
    item: Item = data.get("item")
    await item.create()
    await call.message.answer(_("The product was successfully created."))
    await state.reset_state()


@dp.message_handler(user_id=admins, commands=["mail"])
async def mailing(message: types.Message):
    await message.answer(_("Send the text of mailing"))
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

    await message.answer(_("Choose a language\n\n"
                           "Text:\n"
                           "{text}").format(text=text),
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
    await call.message.answer(_("Mailing Completed"))
