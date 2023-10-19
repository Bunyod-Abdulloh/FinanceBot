from aiogram import types

from data.config import ADMINS
from keyboards.inline.out_keyboards import categories_keyboard
from loader import dp, db


@dp.callback_query_handler(text='outgoing', state='*')
async def outgoing_(call: types.CallbackQuery):

    user_id = str(call.from_user.id)
    all_summary = await db.get_sum_all_out(user_id=call.from_user.id)

    if user_id in ADMINS:
        user_id = int(ADMINS[0])
    else:
        user_id = int(user_id)

    await call.message.edit_text(
        text=f"<b>📤 Chiqim</b>"
             f"\n\n📤 Chiqim bo'limi uchun jami harajat: <b>{all_summary} so'm</b>",
        reply_markup=await categories_keyboard(user_id=user_id)
    )


