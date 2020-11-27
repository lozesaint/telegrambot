import asyncio
from utils.set_bot_commands import set_default_commands

from loader import bot
from utils.db_api.database import create_db
from data.config import admins


# async def on_shutdown(dp):
#     await bot.close()


async def on_startup(dp):
    import filters
    import middlewares
    filters.setup(dp)
    middlewares.setup(dp)

    from utils.notify_admins import on_startup_notify

    await create_db()
    await bot.send_message(admins, "Я запущен!")

    await set_default_commands(dp)
    await on_startup_notify(dp)


if __name__ == '__main__':
    from aiogram import executor
    from admin_panel import dp
    from handlers import dp

    executor.start_polling(dp, on_startup=on_startup, skip_updates=True)

