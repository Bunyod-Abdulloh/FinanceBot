from aiogram import types

from loader import dp

@dp.callback_query_handler(text_contains="addincoming_", state="*")
async def asi_add_summary(call: types.CallbackQuery):
    print(call)
