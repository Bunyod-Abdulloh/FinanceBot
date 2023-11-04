from aiogram import executor

from data.config import ADMINS
from loader import dp, db
import middlewares, filters, handlers
from utils.notify_admins import on_startup_notify
from utils.set_bot_commands import set_default_commands


async def on_startup(dispatcher):
    await db.create()
    # await db.drop_users()
    await db.drop_table_out()
    await db.drop_table_inc()
    # await db.create_table_users()
    await db.create_table_outgoing()
    await db.create_table_incoming()

    await db.add_incoming(user_id=1041847396,
                          incoming_name="Salom",
                          summary=15)

    await set_default_commands(dispatcher)

    await on_startup_notify(dispatcher)


if __name__ == "__main__":
    executor.start_polling(dp, on_startup=on_startup)
