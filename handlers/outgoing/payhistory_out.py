from aiogram import types
from aiogram.dispatcher import FSMContext

from loader import dp


@dp.callback_query_handler(text_contains="payhistory", state="*")
async def phout_history(call: types.CallbackQuery, state: FSMContext):

    product_id = int(call.data.split("_")[1])
    print(call.data)
