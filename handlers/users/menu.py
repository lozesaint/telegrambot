from aiogram import types

from aiogram.dispatcher.filters import Command
from aiogram.types import ReplyKeyboardRemove

from keyboards.default import menu_keyboard, catalog_keyboard
from loader import dp


@dp.message_handler(Command("menu"), content_types="text")
async def show_menu(message: types.Message):
    await message.answer("Choose something from below: ", reply_markup=menu_keyboard)


@dp.message_handler(text_contains="Catalog")
async def show_catalog(message: types.Message):
    await message.answer("Let us get started", reply_markup=catalog_keyboard)

    @dp.message_handler(text_contains="Trending")
    async def show_catalog_trending(message: types.Message):
        await message.answer("You chose Catalog -> Trending")

    @dp.message_handler(text_contains="Tops")
    async def show_catalog_tops(message: types.Message):
        await message.answer("You chose Catalog -> Tops")

    @dp.message_handler(text_contains="Bottoms")
    async def show_catalog_bottoms(message: types.Message):
        await message.answer("You chose Catalog -> Bottoms")

    @dp.message_handler(text_contains="Dresses")
    async def show_catalog_dresses(message: types.Message):
        await message.answer("You chose Catalog -> Dresses")

    @dp.message_handler(text_contains="Shoes")
    async def show_catalog_shoes(message: types.Message):
        await message.answer("You chose Catalog -> Shoes")

    @dp.message_handler(text_contains="Outwear")
    async def show_catalog_outwear(message: types.Message):
        await message.answer("You chose Catalog -> Outwear")

    @dp.message_handler(text_contains="Brand")
    async def show_catalog_brand(message: types.Message):
        await message.answer("You chose Catalog -> Brands")


@dp.message_handler(text_contains="Feedback")
async def show_feedback(message: types.Message):
    await message.answer("You chose Feedback")


@dp.message_handler(text_contains="About")
async def show_about(message: types.Message):
    await message.answer("You chose About")


@dp.message_handler(text_contains="Cart")
async def show_cart(message: types.Message):
    await message.answer("You chose Cart")


@dp.message_handler(text_contains="Settings")
async def show_settings(message: types.Message):
    await message.answer("You chose Settings")

