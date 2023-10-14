from aiogram import types

from data.config import ADMINS
from keyboards.inline.out_keyboards import categories_keyboard
from loader import dp, db


@dp.callback_query_handler(text='outgoing', state='*')
async def outgoing_(call: types.CallbackQuery):

    user_id = str(call.from_user.id)

    if user_id in ADMINS:
        user_id = int(ADMINS[0])
    else:
        user_id = int(user_id)

    await call.message.edit_text(
        text='Chiqimlar bo\'limi',
        reply_markup=await categories_keyboard(user_id=user_id)
    )


