from aiogram import types, Bot
from typing import List
from .models import Item, User, Cart, Order
from .database import db
from sqlalchemy import and_, sql


async def add_item(**kwargs):
    newitem = await Item(**kwargs).create()
    return newitem


async def get_categories() -> List[Item]:
    return await Item.query.distinct(Item.category_code).gino.all()


# async def get_subcategories(category) -> List[Item]:
#     return await Item.query.distinct(Item.subcategory_code).where(Item.category_code == category).gino.all()


async def count_items(category_code, subcategory_code=None):
    conditions = [Item.category_code == category_code]

    if subcategory_code:
        conditions.append(Item.subcategory_code == subcategory_code)

    total = await db.select([db.func.count()]).where(
        and_(*conditions)
    ).gino.scalar()

    return total


async def get_item(item_id) -> Item:
    item = await Item.query.where(Item.id == item_id).gino.first()

    return item


class DBCommands:
    async def get_user(self, user_id) -> User:
        user = await User.query.where(User.user_id == user_id).gino.first()
        return user

    async def get_items(self, category_code) -> List[Item]:
        items = await Item.query.where(Item.category_code == category_code).gino.all()
        return items

    async def get_all_items(self) -> List[Item]:
        items = await Item.query.gino.all()
        return items

    async def user_exists(self, user_id):
        user = await self.get_user(user_id)
        return user

    async def add_new_user(self, referral=None) -> User:
        user = types.User.get_current()
        old_user = await self.get_user(user.id)
        if old_user:
            return old_user
        new_user = User()
        new_user.user_id = user.id
        new_user.username = user.username
        new_user.full_name = user.full_name
        if referral:
            new_user.referral = referral
        await new_user.create()
        return new_user

    async def create_cart_item(self, item_id, chat_id, size, quantity) -> Cart:
        cart = Cart()
        cart.item_id = item_id
        cart.chat_id = chat_id
        cart.size = size
        cart.quantity = quantity
        await cart.create()
        return cart

    async def get_cart_items(self, chat_id):
        cart_items = await Cart.query.where(Cart.chat_id == chat_id).gino.all()
        return cart_items

    async def delete_cart_item(self, chat_id, item_id):
        cart_item = await Cart.query.where(and_(Cart.chat_id == chat_id,
                                                Cart.item_id == item_id)).gino.first()
        await cart_item.delete()

    async def clear_cart(self, chat_id):
        cart_items = await Cart.query.where(Cart.chat_id == chat_id).gino.all()
        for cart_item in cart_items:
            await cart_item.delete()

    async def set_language(self, language):
        user_id = types.User.get_current().id
        user = await self.get_user(user_id)
        await user.update(language=language).apply()

    async def count_users(self):
        total = await db.func.count(User.id).gino.scalar()
        return total

    async def check_referrals(self):
        bot = Bot.get_current()
        user_id = types.User.get_current().id
        user = await self.get_user(user_id)
        referrals = await User.query.where(User.referral == user.id).gino.all()
        return ", ".join([
            f"{num + 1}. " + (await bot.get_chat(referral.user_id)).get_mention(as_html=True)
            for num, referral in enumerate(referrals)
        ])

    async def show_items(self):
        items = await Item.query.gino.all()
        return items

    async def set_feedback(self, feedback):
        user_id = types.User.get_current().id
        user = await self.get_user(user_id)
        await user.update(feedback=feedback).apply()

    async def set_name(self, full_name):
        user_id = types.User.get_current().id
        user = await self.get_user(user_id)
        await user.update(full_name=full_name).apply()

    async def set_phone_number(self, phone_number):
        user_id = types.User.get_current().id
        user = await self.get_user(user_id)
        await user.update(phone_number=phone_number).apply()

    async def set_location(self, location):
        user_id = types.User.get_current().id
        user = await self.get_user(user_id)
        await user.update(address=location).apply()

    async def set_item_status(self, item_id, status):
        item = await get_item(item_id)
        await item.update(active=status).apply()

    async def create_order(self, item_ids, sum, is_cash):
        order = Order()
        order.item_ids = item_ids
        order.sum = sum
        order.is_cash = is_cash
        await order.create()
        return order

    async def get_order(self, order_id) -> Order:
        order = await Order.query.where(Order.id == order_id).gino.first()
        return order

    async def update_order(self, order_id, status):
        order = await self.get_order(order_id)
        await order.update(status=status).apply()
