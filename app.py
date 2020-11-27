from utils.notify_admins import on_startup_notify
from utils.set_bot_commands import set_default_commands
from utils.db_api.database import create_db


async def on_startup(dp):
    import filters
    import middlewares
    filters.setup(dp)
    middlewares.setup(dp)

    await set_default_commands(dp)
    await on_startup_notify(dp)

    await create_db()


if __name__ == '__main__':
    from aiogram import executor
    from admin_panel import dp
    from handlers import dp

    executor.start_polling(dp, on_startup=on_startup, skip_updates=True)
