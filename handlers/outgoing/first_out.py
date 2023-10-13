from aiogram import types

from keyboards.inline.out_keyboards import categories_keyboard
from loader import dp, db


@dp.callback_query_handler(text='outgoing', state='*')
async def outgoing_(call: types.CallbackQuery):

    await call.message.edit_text(
        text='Chiqimlar bo\'limi',
        reply_markup=await categories_keyboard()
    )
