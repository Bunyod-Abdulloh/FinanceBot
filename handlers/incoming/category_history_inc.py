from aiogram import types

from loader import dp


@dp.callback_query_handler(text_contains="historyinc_", state="*")
async def chi_history(call: types.CallbackQuery):
    incoming_name = call.data.split("_")[1]
