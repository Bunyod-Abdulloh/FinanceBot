from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboards.inline.out_keyboards import categories_keyboard
from loader import dp, db
from states.user_states import FinanceEdit


@dp.callback_query_handler(text_contains='editcategory', state='*')
async def edit_category_(call: types.CallbackQuery, state: FSMContext):

    await call.message.delete()

    category_name = call.data.split('_')[-1]

    await state.update_data(
        old_category=category_name
    )

    await call.message.answer(
        text=f'Category_name: {category_name}'
             f'\n\nKategoriya uchun yangi nom kiriting:'
    )

    await FinanceEdit.category.set()


@dp.message_handler(state=FinanceEdit.category)
async def state_edit_category(message: types.Message, state: FSMContext):
    data = await state.get_data()

    await db.update_category_name(
        old_category=data['old_category'],
        new_category=message.text
    )

    await message.answer(
        text='Kategoriya nomi o\'zgartirildi!',
        reply_markup=await categories_keyboard()
    )
    await state.finish()
