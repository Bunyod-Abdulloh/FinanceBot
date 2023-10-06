from aiogram import executor

from loader import dp, db
import middlewares, filters, handlers
from utils.notify_admins import on_startup_notify
from utils.set_bot_commands import set_default_commands


async def on_startup(dispatcher):
    await db.create()
    # await db.drop_users()
    await db.drop_products()
    # await db.create_table_users()
    await db.create_table_finance()
    price = 5000
    item = 9
    await db.add_all(category_name='Bozorlik',
                     productname='Qizilolu',
                     price=price,
                     item=item,
                     summary=price * item)

    await set_default_commands(dispatcher)

    await on_startup_notify(dispatcher)


if __name__ == "__main__":
    executor.start_polling(dp, on_startup=on_startup)
