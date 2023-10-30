from aiogram import types

from loader import dp


@dp.callback_query_handler(text="", state="*")
async def mh_history(call: types.CallbackQuery):
    await call.message.edit_text(
        text="history"
    )
