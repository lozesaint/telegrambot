from aiogram import types

from data.config import admins


async def set_default_commands(dp):
    await dp.bot.set_my_commands([
        types.BotCommand("start", "Start MustHave Official's Bot"),
        types.BotCommand("menu", "Show Main Menu")
    ])
