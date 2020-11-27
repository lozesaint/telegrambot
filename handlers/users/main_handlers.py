from asyncio import sleep
import datetime
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import CommandStart
from aiogram.types import (Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery,
                           LabeledPrice, PreCheckoutQuery)
from aiogram.utils.callback_data import CallbackData

from utils.db_api import database
from states import states
from data.config import PM_TOKEN, admins
from loader import dp, bot, _


db = database.DBCommands()

buy_item = CallbackData("buy", "item_id")


@dp.message_handler(CommandStart)
async def register_user(message: Message):
    chat_id = message.from_user.id
    referral = message.get_args()
    user = await db.add_new_user(referral=referral)
    id = user.id
    bot_username = (await bot.me).username
    bot_link = f"https://t.me/{bot_username}?start={id}"
    count_users = await db.count_users()

    languages_markup = types.InlineKeyboardMarkup(
        inline_keyboard=[
            [types.InlineKeyboardButton(
                text="English",
                callback_data="lang_en")],
            [types.InlineKeyboardButton(
                text="Русский",
                callback_data="lang_ru")],
            [types.InlineKeyboardButton(
                text="O'zbek tili",
                callback_data="lang_uz")]
        ]
    )

    text = _("Greetings!\n"
             "There are {count_users} users right now in our DB\n"
             "\n"
             "Your referral link: {bot_link}\n"
             "Check your referrals by pressing /referrals\n"
             "View items: /items").format(
        count_users=count_users,
        bot_link=bot_link,
    )
    if message.from_user.id == admins:
        text += _("\n"
                  "Add new item: /add_item")

    await message.answer(text, reply_markup=languages_markup)


@dp.callback_query_handler(text_contains="lang")
async def change_language(call: CallbackQuery):
    await call.message.edit_reply_markup()
    lang = call.data[-2:]
    await db.set_language(lang)
    await call.message.answer(_("Your language has been changed", locale=lang))


@dp.message_handler(commands=["referrals"])
async def check_referrals(message: Message):
    referrals = await db.check_referrals()
    text = _("Your referrals:\n{referrals}").format(referrals=referrals)
    await message.answer(text)


@dp.message_handler(commands=["items"])
async def show_items(message: Message):
    all_items = await db.show_items()

    text = _("<b>Item:</b \t№{id}: <u>{name}</u>\n"
             "<b>Price:</b> \t{price:,}\n")

    for item in all_items:
        markup = types.InlineKeyboardMarkup(
            inline_keyboard=[
                [types.InlineKeyboardButton(
                    text=_("Buy"),
                    callback_data=buy_item.new(item_id=item.id))],
            ]
        )

        await message.answer_photo(
            photo=item.photo,
            caption=text.format(id=item.id,
                                name=item.name,
                                price=item.price),
            reply_markup=markup
        )

        await sleep(0.3)


@dp.callback_query_handler(buy_item.filter())
async def buying_item(call: CallbackQuery, callback_data: dict, state: FSMContext):
    item_id = int(callback_data.get("item_id"))
    await call.message.edit_reply_markup()
    item = await database.Item.get("item_id")

    if not item:
        await call.message.answer(_("This item doesnt exists"))
        return

    text = _("Do you want to buy item \"<b>{name}{/b}\" with the price <i>{price:,}</i>\n"
             "Enter the quantity of the item you would like to buy or press /cancel").format(name=item.name,
                                                                                             price=item.price)

    await call.message.answer(text)

    await states.Purchase.EnterQuantity.set()

    await state.update_data(
        item=item,
        purchase=database.Purchase(
            item_id=item_id,
            purchase_time=datetime.datetime.now(),
            buyer=call.from_user.id
        )
    )


@dp.message_handler(regexp=r"^(/d+)$", state=states.Purchase.EnterQuantity)
async def enter_quantity(messsage: Message, state: FSMContext):
    quantity = int(messsage.text)
    async with state.proxy() as data:
        data["purchase"].quantity = quantity
        item = data.get("item")
        amount = item.price * quantity
        data["purchase"].amount = amount

    agree_button = InlineKeyboardButton(
        text=_("Agree"),
        callback_data="agree"
    )
    change_button = InlineKeyboardButton(
        text=_("Change the quantity"),
        callback_data="change"
    )
    cancel_button = InlineKeyboardButton(
        text=_("Cancel purchase"),
        callback_data="cancel"
    )

    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [agree_button],
            [change_button],
            [cancel_button]
        ]
    )

    await messsage.answer(
        _("Okay, you want to buy <i>{quantity}</i> {name} with price <b>{price:,}</b>\n"
          "Total price: <b>{amount:,}</b>. Confirm?").format(
            quantity=quantity,
            name=item.name,
            amount=amount,
            price=item.price
        ),
        reply_markup=markup
    )

    await states.Purchase.Approval.set()


@dp.message_handler(state=states.Purchase.EnterQuantity)
async def wrong_input(message: Message):
    await message.answer(_("Wrong Input, enter a number"))


@dp.callback_query_handler(text_contains="cancel", state=states.Purchase.Approval)
async def cancel_purchase(call: CallbackQuery, state: FSMContext):
    await call.message.edit_reply_markup()
    await call.message.answer(_("Purchase Canceled."))
    await state.reset_state()


@dp.callback_query_handler(text_contains="change", state=states.Purchase.Approval)
async def change_purchase(call: CallbackQuery, state: FSMContext):
    await call.message.edit_reply_markup()
    await call.message.answer(_("Enter the quantity again."))
    await states.Purchase.EnterQuantity.set()


@dp.callback_query_handler(text_contains="agree", state=states.Purchase.Approval)
async def change_purchase(call: CallbackQuery, state: FSMContext):
    await call.message.edit_reply_markup()
    data = await state.get_data()
    purchase = data.get("purchase")
    item = data.get("item")

    await purchase.create()

    await call.message.answer(_("Okay, pay <b>{amount:,}</b> by the method below and press the button below").format(amount=purchase.amount))

    currency = "UZS"
    need_name = True
    need_phone_number = True
    need_shipping_address = True

    await bot.send_invoice(
        chat_id=call.from_user.id,
        title=item.name,
        description=item.name,
        payload=str(purchase.id),
        start_parameter=str(purchase.id),
        currency=currency,
        prices=[
            LabeledPrice(label=item.name,
                         amount=purchase.amount)
        ],
        provider_token=PM_TOKEN,
        need_name=need_name,
        need_phone_number=need_phone_number,
        need_shipping_address=need_shipping_address,
    )

    await state.update_data(purchase=purchase)
    await states.Purchase.Payment.set()


@dp.pre_checkout_query_handler(state=states.Purchase.Payment)
async def checkout(query: PreCheckoutQuery, state: FSMContext):
    await bot.answer_pre_checkout_query(query.id, True)
    data = await state.get_data()
    purchase: database.Purchase = data.get("purchase")
    success = await check_payment(purchase)
    if success:
        await purchase.update(
            successful=True,
            shipping_address=query.order_info.shipping_address.to_python()
            if query.order_info.shipping_address else None,
            phone_number=query.order_info.phone_number,
            receiver=query.order_info.name
        ).apply()

        await state.reset_state()

        await bot.send_message(chat_id=query.from_user.id,
                               text=_("Thank you for your purchase"))
    else:
        await bot.send_message(chat_id=query.from_user.id,
                               text=_("Purchase failed, try again later.."))


async def check_payment(purchase: database.Purchase):
    return True


@dp.message_handler()
async def echo(message: Message):
    await message.answer(message.text)
