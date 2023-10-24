from aiogram import types

from loader import dp


@dp.callback_query_handler(text="incoming", state="*")
async def incoming_main_menu(call: types.CallbackQuery):

