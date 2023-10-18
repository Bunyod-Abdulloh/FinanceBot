from aiogram import types
from aiogram.dispatcher import FSMContext

from handlers.all.all_functions import replace_point_bottom_line, warning_text
from keyboards.inline.out_keyboards import categories_keyboard
from loader import dp, db
from states.user_states import FinanceEdit


@dp.callback_query_handler(text_contains='editsubcategory', state='*')
async def state_edit_subcategory(call: types.CallbackQuery, state: FSMContext):

    await call.message.delete()

    old_subcategory = call.data.split('_')[1]

    await state.update_data(
        old_subcategory=old_subcategory
    )

    await call.message.answer(
        text=f'Subkategoriya: {old_subcategory}'
             f'\n\n{warning_text}'
             f'\n\nSubkategoriya uchun yangi nom kiriting:'
    )
    await FinanceEdit.subcategory.set()


@dp.message_handler(state=FinanceEdit.subcategory)
async def state_edit_subcategory_(message: types.Message, state: FSMContext):

    new_subcategory = await replace_point_bottom_line(message=message.text)

    data = await state.get_data()

    await db.update_subcategoryname_out(
        user_id=message.from_user.id,
        old_subcategory=data['old_subcategory'],
        new_subcategory=new_subcategory
    )

    await message.answer(
        text='Subkategoriya nomi o\'zgartirildi!',
        reply_markup=await categories_keyboard(user_id=message.from_user.id)
    )
    await state.finish()
