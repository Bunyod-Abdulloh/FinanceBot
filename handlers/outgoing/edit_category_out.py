import re

from aiogram import types
from aiogram.dispatcher import FSMContext

from handlers.all.all_functions import warning_text_uz_latin, warning_number_uz_latin
from keyboards.inline.outgoing_keyboards import categories_keyboard
from loader import dp, db
from states.user_states import FinanceEdit


@dp.callback_query_handler(text='editcategory', state='*')
async def edit_category_(call: types.CallbackQuery, state: FSMContext):

    data = await state.get_data()

    await call.message.edit_text(
        text=f"Kategoriya: <b>{data['category']}</b>"
             f"\n\n{warning_text_uz_latin}"
             f"\n\nKategoriya uchun yangi nom kiriting:"

    )
    await FinanceEdit.category.set()


@dp.message_handler(state=FinanceEdit.category)
async def state_edit_category(message: types.Message, state: FSMContext):
    text = re.sub(r"[^\w\s]", "", message.text)
    summary = await db.get_sum_all_out(
        user_id=message.from_user.id
    )
    data = await state.get_data()

    await db.update_categoryname_out(
        user_id=message.from_user.id,
        old_category=data['category'],
        new_category=text
    )

    await message.answer(
        text='Kategoriya nomi o\'zgartirildi!')

    await message.edit_text(
        text=f"📤 Chiqim"
             f"\n\n📤 Chiqim uchun jami harajat: {summary} so'm",
        reply_markup=await categories_keyboard(
            user_id=message.from_user.id)
    )
    await state.finish()
