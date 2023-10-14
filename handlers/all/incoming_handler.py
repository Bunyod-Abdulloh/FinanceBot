from aiogram import types

from loader import dp


@dp.callback_query_handler(text='incoming', state='*')
async def incoming_(call: types.CallbackQuery):

    await call.answer(
        text='Kirimlar bo\'limi',
        show_alert=True
    )
