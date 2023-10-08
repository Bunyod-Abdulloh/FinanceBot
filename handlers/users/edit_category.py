from aiogram import types
from aiogram.dispatcher import FSMContext

import states.user_states
from keyboards.inline.menu_keyboards import categories_keyboard
from loader import dp, db
from states.user_states import FinanceEditCategory


@dp.callback_query_handler(text_contains='editcategory', state='*')
async def edit_category_(call: types.CallbackQuery, state: FSMContext):

    category_name = call.data.split('_')[-1]

    await call.message.answer(
        text=f'Category_name: {category_name}'
             f'\n\nKategoriya uchun yangi nom kiriting:'
    )

    await FinanceEditCategory.one.set()


@dp.message_handler(state=FinanceEditCategory.one)
async def state_edit_category(message: types.Message, state: FSMContext):

    await db.update_category_name(
        category_name=message.text
    )

    await message.answer(
        text='Kategoriya nomi o\'zgartirildi!',
        reply_markup=await categories_keyboard()
    )
    await state.finish()
