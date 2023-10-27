import logging

from aiogram import types
from aiogram.dispatcher import FSMContext

from handlers.all.all_functions import replace_point_bottom_line, warning_text
from keyboards.inline.outgoing_keyboards import items_keyboard, subcategories_keyboard
from loader import dp, db
from states.user_states import FinanceEdit


@dp.callback_query_handler(text='editsubcategory', state='*')
async def state_edit_subcategory(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()

    await call.message.edit_text(
        text=f'Subkategoriya: {data["subcategory"]}'
             f'\n\n{warning_text}'
             f'\n\nSubkategoriya uchun yangi nom kiriting:'
    )
    await FinanceEdit.subcategory.set()


@dp.message_handler(state=FinanceEdit.subcategory)
async def state_edit_subcategory_(message: types.Message, state: FSMContext):
    try:
        new_subcategory = await replace_point_bottom_line(message=message.text)

        data = await state.get_data()
        user_id = message.from_user.id
        category = data['category']
        subcategory = data['subcategory']

        await db.update_subcategoryname_out(
            user_id=user_id,
            old_subcategory=subcategory,
            new_subcategory=new_subcategory
        )

        await message.answer(
            text='Subkategoriya nomi o\'zgartirildi!'
        )

        await message.answer(
            text=f"<b>📤 Chiqim > {category}</b>",
            reply_markup=await subcategories_keyboard(
                category_name=category,
                user_id=user_id
            )
        )
        await state.finish()
    except Exception as err:
        logging.error(err)
