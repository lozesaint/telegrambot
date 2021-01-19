from typing import Union

from aiogram.dispatcher import FSMContext
from aiogram.types import InlineQuery, CallbackQuery, Message, ReplyKeyboardRemove
from aiogram import types
from geopy.geocoders import Nominatim

from data.config import admins
from handlers.users.main_menu import show_menu
from keyboards.default import get_contact_keyboard, get_location_keyboard
from keyboards.inline.callback_datas import back_to_menu, quantity_cd, cart_delete_cd, pay_method_cd
from keyboards.inline import get_item_keyboard, get_size_keyboard, get_cart_keyboard, get_categories_keyboard
from keyboards.inline.payment_keyboard import get_payment_keyboard
from keyboards.inline.quantity_keyboard import get_quantity_keyboard
from keyboards.inline.order_keyboard import order_keyboard_phase_0, get_order_keyboard_phase_1, get_order_keyboard_phase_2, order_keyboard_phase_3
from loader import dp, bot, _
from states.states import Menu, Item, Order
from utils.db_api import db_commands
from utils.misc.number_refactoring import refactor

db = db_commands.DBCommands()

category_associations = {
    '👚': 'shirts',
    '👗': 'dresses',
    '🥻': 'sundresses',
    '👖': 'trousers',
    '🩳': 'skirts',
    '📦': 'other'
}


@dp.inline_handler(state=Menu.Category, text=["👚", "👗", "🥻", "👖", "🩳", "📦", "🏪"])
async def show_category_items(query: Union[InlineQuery, CallbackQuery]):
    category = query.query
    result = []

    if category == '🏪':
        items = await db.get_all_items()
    else:
        items = await db.get_items(category_associations[category])

    for item in items:
        if str(query.from_user.id) in admins:
            result.append(types.InlineQueryResultCachedPhoto(
                id=item.id,
                photo_file_id=item.photo,
                input_message_content=types.InputTextMessageContent(
                    message_text=item.id
                )
            ))
        else:
            if item.active is True:
                result.append(types.InlineQueryResultCachedPhoto(
                    id=item.id,
                    photo_file_id=item.photo,
                    input_message_content=types.InputTextMessageContent(
                        message_text=item.id
                    )
                ))

    await query.answer(
        results=result
    )


"""
HANDLERS FOR ITEM
"""


@dp.message_handler(content_types=types.ContentTypes.TEXT, state=[Menu.Category, Menu.Item])
async def show_item(message: Message, state: FSMContext):
    user = await db.get_user(message.from_user.id)
    item_id = message.text
    item = await db_commands.get_item(int(item_id))

    text = _("<b>{name}</b>"
             "\n\n<b>Price:</b> {price} UZS "
             "\n<b>Sizes:</b> {available_sizes} "
             "\n\nFor all related questions text @g_continent\n\n").format(name=item.name,
                                                                           price=item.price,
                                                                           available_sizes=item.available_sizes)

    photo = await bot.send_photo(chat_id=message.from_user.id,
                                 photo=item.photo,
                                 caption=text,
                                 reply_markup=get_item_keyboard(item.category_name, item.id, message.from_user.id, item.active, user.language))

    data = await state.get_data()
    message_ids = data.get('message_ids')

    if message_ids:
        message_ids.append(photo.message_id)
    else:
        message_ids = [photo.message_id]

    await state.update_data(message_ids=message_ids)

    await bot.delete_message(chat_id=message.from_user.id,
                             message_id=message.message_id)

    await Menu.Item.set()


@dp.callback_query_handler(text_contains="disable_item_", user_id=admins, state=Menu.Item)
async def disable_item(call: CallbackQuery):
    user = await db.get_user(call.from_user.id)
    item_id = int(call.data[13:])
    item = await db_commands.get_item(item_id)

    await db.set_item_status(item_id, False)

    await bot.edit_message_reply_markup(chat_id=call.from_user.id,
                                        message_id=call.message.message_id,
                                        reply_markup=get_item_keyboard(item.category_name, item_id, call.from_user.id, False, user.language))

    await call.answer()


@dp.callback_query_handler(text_contains="enable_item_", user_id=admins, state=Menu.Item)
async def enable_item(call: CallbackQuery):
    user = await db.get_user(call.from_user.id)
    item_id = int(call.data[12:])
    item = await db_commands.get_item(item_id)

    await db.set_item_status(item_id, True)

    await bot.edit_message_reply_markup(chat_id=call.from_user.id,
                                        message_id=call.message.message_id,
                                        reply_markup=get_item_keyboard(item.category_name, item_id, call.from_user.id, True, user.language))

    await call.answer()


@dp.callback_query_handler(text_contains="add_item", state=[Menu.Item, Item.Quantity])
async def show_sizes(call: types.CallbackQuery, state: FSMContext):
    item_id = int(call.data[9:])

    data = await state.get_data()
    message_ids = data.get('message_ids')
    print(message_ids)

    await state.update_data(item_id=item_id)

    await bot.edit_message_reply_markup(chat_id=call.from_user.id,
                                        reply_markup=await get_size_keyboard(item_id),
                                        message_id=call.message.message_id)

    await call.answer()

    await Item.Size.set()


@dp.callback_query_handler(state=Item.Size, text_contains="chosen")
async def choose_quantity(call: CallbackQuery, state: FSMContext):
    size = call.data[7:]

    data = await state.get_data()
    item_id = data.get('item_id')

    cart_items = await db.get_cart_items(call.from_user.id)
    for cart_item in cart_items:
        item = await db_commands.get_item(int(cart_item.item_id))
        if item_id == item.id and cart_item.size == size:
            await call.answer(text=_("Product with same size already exists in the cart"), show_alert=True)
            return

    await state.update_data(size=size)

    await call.message.edit_reply_markup(get_quantity_keyboard(amount=0))

    await Item.Quantity.set()


@dp.callback_query_handler(quantity_cd.filter(action="plus"), state=Item.Quantity)
async def plus_quantity(call: CallbackQuery, callback_data: dict):
    amount = int(callback_data['amount'])
    amount += 1

    await call.message.edit_reply_markup(get_quantity_keyboard(amount))


@dp.callback_query_handler(quantity_cd.filter(action="minus"), state=Item.Quantity)
async def minus_quantity(call: CallbackQuery, callback_data: dict):
    amount = int(callback_data['amount'])

    if amount == 0:
        await call.answer()
        return
    else:
        amount -= 1

    await call.message.edit_reply_markup(get_quantity_keyboard(amount))


@dp.callback_query_handler(text="none", state="*")
async def action_none(call: CallbackQuery):
    await call.answer()


@dp.callback_query_handler(quantity_cd.filter(action="add_to_cart"), state=Item.Quantity)
async def adding_to_cart(call: CallbackQuery, callback_data: dict, state: FSMContext):
    quantity = int(callback_data['amount'])
    data = await state.get_data()
    item_id = data.get('item_id')
    size = data.get('size')
    message_ids = data.get('message_ids')

    if quantity == 0:
        await call.answer(text=_("Item's number should be greater than 0"), show_alert=True)
        return
    else:
        await db.create_cart_item(str(item_id), chat_id=call.from_user.id, quantity=quantity, size=size)
        await call.answer(text=_("Item has been added to cart"), show_alert=True)
        for message_id in message_ids:
            await bot.delete_message(chat_id=call.from_user.id, message_id=message_id)
        message_ids = []
        await state.update_data(message_ids=message_ids)

    await Menu.Category.set()


"""
HANDLERS FOR CART
"""


@dp.callback_query_handler(state=Menu.Category, text="show_cart")
async def show_cart(call: Union[CallbackQuery, Message], edit=False):
    cart_items = await db.get_cart_items(call.from_user.id)

    if isinstance(call, Message):
        message_id = call.message_id
    else:
        message_id = call.message.message_id

    if len(cart_items) == 0:
        await call.answer(text=_("Your cart is empty"), show_alert=True)
        if edit:
            await bot.delete_message(chat_id=call.from_user.id, message_id=message_id)
        return

    text = _("<i>Your Cart:</i>\n\n")

    total = 0
    items = []
    for index, cart_item in enumerate(cart_items, 1):
        item = await db_commands.get_item(int(cart_item.item_id))
        items.append(item)
        text += _("<b>{index}.</b> {name} - <b>{size}</b>\n").format(index=index, name=item.name, size=cart_item.size)
        text += f"\t\t\t{cart_item.quantity} × {item.price} = {refactor(int(item.price.replace(' ', '')) * cart_item.quantity)} UZS\n\n"
        total += int(item.price.replace(" ", "")) * cart_item.quantity

    text += _("<b>Total</b>: {total} UZS").format(total=refactor(total))

    if not edit:
        await bot.delete_message(chat_id=call.from_user.id, message_id=message_id)
        await bot.send_message(chat_id=call.from_user.id,
                               text=text, reply_markup=get_cart_keyboard(items))
    else:
        await bot.edit_message_text(text=text, chat_id=call.from_user.id, message_id=call.message.message_id)
        await bot.edit_message_reply_markup(chat_id=call.from_user.id, message_id=call.message.message_id,
                                            reply_markup=get_cart_keyboard(items))

    if isinstance(call, CallbackQuery):
        await call.answer()

    await Menu.Cart.set()


@dp.callback_query_handler(cart_delete_cd.filter(), state=Menu.Cart)
async def delete_items(call: CallbackQuery):
    user = await db.get_user(call.from_user.id)
    item_id = call.data[19:]
    await db.delete_cart_item(item_id=item_id, chat_id=call.from_user.id)
    await show_cart(call, edit=True)
    cart_items = await db.get_cart_items(call.from_user.id)
    if len(cart_items) == 0:
        await bot.send_message(chat_id=call.from_user.id,
                               text=_('Categories Menu:'),
                               reply_markup=get_categories_keyboard(user.language))
        await Menu.Category.set()


@dp.callback_query_handler(state=Menu.Cart, text="clear_cart")
async def clear_cart(call: CallbackQuery):
    user = await db.get_user(call.from_user.id)
    await db.clear_cart(chat_id=call.from_user.id)
    await show_cart(call, edit=True)
    await bot.send_message(chat_id=call.from_user.id,
                           text=_('Categories Menu:'),
                           reply_markup=get_categories_keyboard(user.language))
    await Menu.Category.set()


"""
HANDLERS FOR ORDER
"""


@dp.callback_query_handler(state=Menu.Cart, text="order")
async def create_order(call: CallbackQuery):
    user = await db.get_user(call.from_user.id)

    await call.message.answer(_("Leave your contact number so we can contact you regarding your order"),
                              reply_markup=get_contact_keyboard(user.language))
    await Order.PhoneNumber.set()
    await call.answer()


@dp.message_handler(state=Order.PhoneNumber, content_types=types.ContentTypes.CONTACT)
async def inputting_number(message: Message):
    user = await db.get_user(message.from_user.id)
    number = message.contact.phone_number
    print(number)
    await db.set_phone_number(number)
    await message.answer(_("Share your current location for the shipping address"),
                         reply_markup=get_location_keyboard(user.language))

    await Order.Location.set()


@dp.message_handler(state=Order.PhoneNumber, regexp="^[+]*[(]{0,1}[0-9]{1,4}[)]{0,1}[-\s\./0-9]*$")
async def inputting_number(message: Message):
    user = await db.get_user(message.from_user.id)
    number = message.text
    await db.set_phone_number(number)
    await message.answer(_("Share your current location for the shipping address"),
                         reply_markup=get_location_keyboard(user.language))

    await Order.Location.set()


@dp.message_handler(state=Order.Location, content_types=types.ContentTypes.LOCATION | types.ContentTypes.TEXT)
async def get_location(message: types.Message):
    user = await db.get_user(message.from_user.id)
    if message.content_type == "location":
        raw_location = message.location
        locator = Nominatim(user_agent="myGeocoder")
        coordinates = [raw_location.latitude, raw_location.longitude]
        location = locator.reverse(coordinates)
        location = location.address
    else:
        location = message.text
        if location == '✖️ Cancel' or location == '✖️ Отменить':
            await bot.send_message(chat_id=message.from_user.id,
                                   text=_('<i>Order cancelled</i>'),
                                   reply_markup=ReplyKeyboardRemove())
            await show_cart(message)
            return

    await db.set_location(location)

    await message.answer(_("Select payment method\n\n<i>*Delivery fee not included</i>"),
                         reply_markup=get_payment_keyboard(user.language))

    await Order.PayMethod.set()


@dp.callback_query_handler(pay_method_cd.filter(), state=Order.PayMethod)
async def pay_method(call: CallbackQuery):
    cart_items = await db.get_cart_items(call.from_user.id)
    user = await db.get_user(call.from_user.id)
    payment_method = call.data[8:].capitalize()

    is_cash = False
    if payment_method == 'Cash':
        is_cash = True
        payment_method = "Наличные"

    text = "<i>Информация о заказе:</i>\n\n" \
           f"<b>Номер Телефона:</b> {user.phone_number}\n\n" \
           f"<b>Адрес Доставки:</b> {user.address}\n\n" \
           f"<b>Метод Оплаты:</b> {payment_method}\n\n"
    total = 0
    item_ids = []
    for index, cart_item in enumerate(cart_items, 1):
        item_ids.append(cart_item.item_id)
        item = await db_commands.get_item(int(cart_item.item_id))
        text += f"<b>{index}.</b> {item.name} - <b>{cart_item.size}</b>\n"
        text += f"\t\t\t{cart_item.quantity} × {item.price} = {refactor(int(item.price.replace(' ', '')) * cart_item.quantity)} СУМ\n\n"
        total += int(item.price.replace(" ", "")) * cart_item.quantity
    text += f"<b>Итого</b>: {refactor(total)} СУМ"

    order = await db.create_order(item_ids=",".join(item_ids), sum=total, is_cash=is_cash)
    text = f"<b>Номер заказа:</b> #N{order.id}\n" + text

    await call.message.answer(text=_("<i>Thank you, your order has been submitted for processing! Our operators will contact you shortly</i>"),
                              reply_markup=ReplyKeyboardRemove())

    await bot.send_message(chat_id="@MustHave_Official",
                           text=text,
                           reply_markup=get_order_keyboard_phase_1(order.id, call.from_user.id))
    await Order.Confirmation.set()
    await call.answer()


@dp.callback_query_handler(text_contains='confirm_', user_id=admins, state='*')
async def confirming(call: CallbackQuery):
    x, order_id, user_id = call.data.split("_")
    order_id = int(order_id)
    user_id = int(user_id)
    order = await db.get_order(order_id)
    await bot.edit_message_reply_markup(chat_id="@MustHave_Official",
                                        message_id=call.message.message_id,
                                        reply_markup=get_order_keyboard_phase_2(order_id, user_id))
    await db.update_order(order_id=order_id, status=1)

    if not order.is_cash:
        await bot.send_message(chat_id=user_id,
                               text=_("<b>Order Number</b>: #N{order_id}\n\n"
                                      "Credit card number for transferring:\n<b>8600 3129 4618 7313</b>").format(order_id=order_id))
    else:
        await bot.send_message(chat_id=user_id,
                               text=_("<b>Order Number</b>: #N{order_id}\n\nYour order has been confirmed.").format(order_id=order_id))


@dp.callback_query_handler(text_contains="cancel_", user_id=admins, state='*')
async def canceling(call: CallbackQuery):
    x, order_id, user_id = call.data.split("_")
    order_id = int(order_id)
    user_id = int(user_id)

    await bot.send_message(chat_id=user_id,
                           text=_("<b>Your order has been cancelled</b>"))

    await db.update_order(order_id=order_id, status=0)
    await bot.edit_message_reply_markup(chat_id="@MustHave_Official",
                                        message_id=call.message.message_id,
                                        reply_markup=order_keyboard_phase_0)

    await db.clear_cart(call.from_user.id)


@dp.callback_query_handler(text_contains="success_", user_id=admins, state='*')
async def successful(call: CallbackQuery):
    x, order_id, user_id = call.data.split("_")
    order_id = int(order_id)
    user_id = int(user_id)

    await bot.send_message(chat_id=user_id,
                           text=_("<b>Your payment has been approved</b>"))

    await db.update_order(order_id=order_id, status=2)
    await bot.edit_message_reply_markup(chat_id="@MustHave_Official",
                                        message_id=call.message.message_id,
                                        reply_markup=order_keyboard_phase_3)

    await db.clear_cart(call.from_user.id)


"""
HANDLERS FOR "BACK" BUTTONS
"""


@dp.callback_query_handler(back_to_menu.filter(action="back_to_main"), state=Menu.Category)
async def back(call: CallbackQuery):
    await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
    await show_menu(call)


@dp.callback_query_handler(back_to_menu.filter(action="back_to_category"), state=[Menu.Item, Menu.Cart])
async def back(call: CallbackQuery, state: FSMContext):
    user = await db.get_user(call.from_user.id)
    current_state = await state.get_state()

    data = await state.get_data()
    message_ids = data.get('message_ids')

    if current_state == "Menu:Item":
        for message_id in message_ids:
            await bot.delete_message(chat_id=call.from_user.id, message_id=message_id)
        message_ids.clear()
        await state.update_data(message_ids=message_ids)
    elif current_state == "Menu:Cart":
        await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
        await bot.send_message(chat_id=call.from_user.id,
                               text='Categories Menu:',
                               reply_markup=get_categories_keyboard(user.language))

    await Menu.Category.set()


@dp.callback_query_handler(text_contains="back_to_item", state=Item.Size)
async def back(call: CallbackQuery):
    user = await db.get_user(call.from_user.id)
    item_id = call.data[13:]
    item = await db_commands.get_item(int(item_id))
    await bot.edit_message_reply_markup(chat_id=call.from_user.id,
                                        message_id=call.message.message_id,
                                        reply_markup=get_item_keyboard(item.category_name, item_id, call.from_user.id, item.active, user.language))
    await Menu.Item.set()


@dp.callback_query_handler(back_to_menu.filter(action="back_to_size"), state=Item.Quantity)
async def back(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    item_id = data["item_id"]
    call.data = "add_item_" + str(item_id)

    await show_sizes(call, state)


@dp.message_handler(state=Order.PhoneNumber, text=["🔙 Back", "🔙 Назад"])
async def back_to_cart(message: Message):
    await bot.send_message(chat_id=message.from_user.id,
                           text=_('<i>Order cancelled</i>'),
                           reply_markup=ReplyKeyboardRemove())
    await show_cart(message)
