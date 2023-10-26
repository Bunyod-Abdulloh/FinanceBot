import logging

from aiogram import types
from aiogram.dispatcher import FSMContext

from handlers.all.all_functions import replace_point_bottom_line, warning_text
from keyboards.inline.outgoing_keyboards import categories_keyboard, items_keyboard
from loader import dp, db
from states.user_states import FinanceEdit


@dp.callback_query_handler(text_contains='editsubcategory', state='*')
async def state_edit_subcategory(call: types.CallbackQuery, state: FSMContext):

    await call.message.delete()

    old_subcategory = call.data.split('_')[1]

    await call.message.answer(
        text=f'Subkategoriya: {old_subcategory}'
             f'\n\n{warning_text}'
             f'\n\nSubkategoriya uchun yangi nom kiriting:'
    )
    await FinanceEdit.subcategory.set()


@dp.message_handler(state=FinanceEdit.subcategory)
async def state_edit_subcategory_(message: types.Message, state: FSMContext):
    try:
        new_subcategory = await replace_point_bottom_line(message=message.text)

        data = await state.get_data()
        category = data['category']
        subcategory = data['subcategory']
        user_id = message.from_user.id

        await db.update_subcategoryname_out(
            user_id=user_id,
            old_subcategory=subcategory,
            new_subcategory=new_subcategory
        )

        await message.answer(
            text='Subkategoriya nomi o\'zgartirildi!'
        )

        await message.answer(
            text=f"<b>📤 Chiqim > {category} > {subcategory}</b>",
            reply_markup=await items_keyboard(
                user_id=user_id,
                category_name=category,
                subcategory_name=subcategory
            )
        )
        print(data)
        await state.finish()
    except Exception as err:
        logging.error(err)
