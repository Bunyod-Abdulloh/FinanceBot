from aiogram import types

from keyboards.inline.menu_keyboards import categories_keyboard
from loader import dp, db

PAGE_COUNT = 25


@dp.callback_query_handler(text='outgoing', state='*')
async def outgoing_(call: types.CallbackQuery):

    await call.message.edit_text(
        text='Chiqimlar bo\'limi',
        reply_markup=await categories_keyboard()
    )
