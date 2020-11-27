from aiogram import types


async def set_default_commands(dp):
    await dp.bot.set_my_commands([
        types.BotCommand("start", "Start MustHave Official's Bot"),
        types.BotCommand("help", "Show Available Commands"),
        types.BotCommand("menu", "Show Main Menu"),
        types.BotCommand("email", "Show Email Menu"),
    ])