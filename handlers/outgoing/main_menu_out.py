from aiogram import types

from handlers.all.all_functions import all_summary_main_out
from loader import dp


@dp.callback_query_handler(text='outgoing', state='*')
async def outgoing_(call: types.CallbackQuery):

    user_id = call.from_user.id

    await all_summary_main_out(
        user_id=user_id,
        callback=call,
        section_name="📤 Chiqim",
        total="📤 Chiqim bo'limi uchun jami harajat",
        currency="so`m"
    )
