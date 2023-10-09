from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboards.inline.menu_keyboards import categories_keyboard
from loader import dp, db
from states.user_states import FinanceEdit


@dp.callback_query_handler(text_contains='editsubcategory', state='*')
async def state_edit_subcategory(call: types.CallbackQuery, state: FSMContext):

    await call.message.delete()

    old_subcategory = call.data.split('_')[-1]

    await state.update_data(
        old_subcategory=old_subcategory
    )

    await call.message.answer(
        text=f'Subcategory_name: {old_subcategory}'
             f'\n\nSubkategoriya uchun yangi nom kiriting:'
             f'\n(YYYY-MM-DD, \nYIL-OY-KUN ko\'rinishida bo\'lishi lozim!)'
    )

    await FinanceEdit.subcategory.set()


@dp.message_handler(state=FinanceEdit.subcategory)
async def state_edit_subcategory_(message: types.Message, state: FSMContext):
    data = await state.get_data()

    await db.update_subcategory_name(
        old_subcategory=data['old_subcategory'],
        new_subcategory=message.text
    )

    await message.answer(
        text='Subkategoriya nomi o\'zgartirildi!',
        reply_markup=await categories_keyboard()
    )

    await state.finish()
