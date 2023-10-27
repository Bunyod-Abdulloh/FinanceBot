from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboards.inline.out_in_keys import check_no_button
from loader import dp, db
from states.user_states import FinanceSubcategory


@dp.callback_query_handler(text_contains="deletesubcategory", state="*")
async def delete_subcategory(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    subcategory = await data['subcategory']

    await call.message.edit_text(
        text=f"E'tibor qiling, o'chirish tugmasini bossangiz {subcategory}dagi barcha ma'lumotlar o'chib ketadi!"
             f"O'chirishni xohlaysizmi?",
        reply_markup=check_no_button
    )
    await FinanceSubcategory.delete_subcategory.set()


@dp.callback_query_handler(state=FinanceSubcategory.delete_subcategory)
async def delete_subcategory_(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    subcategory = data['subcategory']

    if call.data == "yes_delete":
        await db.delete_subcategory_out(
            subcategory=subcategory,
            user_id=call.from_user.id
        )
        await call.answer(
            text="Ma'lumotlar bazadan o'chirildi!",
            show_alert=True
        )

    elif call.data == "no_delete":
        await call.message.edit_text(
            text=f"E'tibor qiling, o'chirish tugmasini bossangiz {subcategory}dagi barcha ma'lumotlar o'chib ketadi!"
                 f"O'chirishni xohlaysizmi?",
            reply_markup=check_no_button
        )
        await FinanceSubcategory.delete_subcategory.set()
