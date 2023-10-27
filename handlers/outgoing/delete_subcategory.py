from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboards.inline.out_in_keys import check_no_button
from keyboards.inline.outgoing_keyboards import items_keyboard, subcategories_keyboard
from loader import dp, db
from states.user_states import FinanceSubcategory


@dp.callback_query_handler(text="deletesub", state="*")
async def ds_delete_subcategory(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    subcategory = data['subcategory']

    await call.message.edit_text(
        text=f"E'tibor qiling, o'chirish tugmasini bossangiz <code>{subcategory}</code>dagi barcha ma'lumotlar o'chib "
             f"ketadi!\n\nO'chirishni xohlaysizmi?",
        reply_markup=check_no_button
    )
    await FinanceSubcategory.delete_subcategory.set()


@dp.callback_query_handler(state=FinanceSubcategory.delete_subcategory)
async def delete_subcategory_(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    user_id = call.from_user.id
    category = data['category']
    subcategory = data['subcategory']

    if call.data == "yes_delete":
        await db.delete_subcategory_out(
            subcategory=subcategory,
            user_id=user_id
        )
        await call.answer(
            text="Ma'lumotlar bazadan o'chirildi!",
            show_alert=True
        )
        await call.message.edit_text(
            text=f"<b>📤 Chiqim > {category} > {subcategory}</b>",
            reply_markup=await subcategories_keyboard(
                category_name=category,
                user_id=user_id
            )
        )

    elif call.data == "no_delete":
        await call.message.edit_text(
            text=f"<b>📤 Chiqim > {category} > {subcategory}</b>",
            reply_markup=await subcategories_keyboard(
                category_name=category,
                user_id=user_id
            )
        )

    await state.finish()
