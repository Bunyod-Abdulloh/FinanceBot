from aiogram import types
from aiogram.dispatcher import FSMContext

from handlers.all.all_functions import replace_point_bottom_line
from keyboards.inline.out_keyboards import categories_keyboard
from loader import dp, db
from states.user_states import FinanceEdit


@dp.callback_query_handler(text_contains='editcategory', state='*')
async def edit_category_(call: types.CallbackQuery, state: FSMContext):

    await call.message.delete()

    category_name = call.data.split('_')[1]

    await state.update_data(
        old_category=category_name
    )

    await call.message.answer(
        text=f'Kategoriya: {category_name}'
             f'\n\nKategoriya uchun yangi nom kiriting:'
    )

    await FinanceEdit.category.set()


@dp.message_handler(state=FinanceEdit.category)
async def state_edit_category(message: types.Message, state: FSMContext):

    new_category = await replace_point_bottom_line(message=message.text)

    data = await state.get_data()

    await db.update_categoryname_out(
        user_id=message.from_user.id,
        old_category=data['old_category'],
        new_category=new_category
    )

    await message.answer(
        text='Kategoriya nomi o\'zgartirildi!',
        reply_markup=await categories_keyboard(user_id=message.from_user.id)
    )
    await state.finish()
