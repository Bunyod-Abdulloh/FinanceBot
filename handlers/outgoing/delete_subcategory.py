from aiogram import types
from aiogram.dispatcher import FSMContext

from loader import dp, db


@dp.callback_query_handler(text_contains="deletesubcategory", state="*")
async def delete_subcategory(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    subcategory = await data['subcategory']

    await call.message.edit_text(
        text=f"E'tibor qiling, o'chirish tugmasini bossangiz {subcategory}dagi barcha ma'lumotlar o'chib ketadi!"
             f"O'chirishni xohlaysizmi?"
    )

    await db.delete_subcategory_out(
        subcategory=subcategory
    )
    await call.answer(
        text="Ma'lumotlar bazadan o'chirildi!",
        show_alert=True
    )

# no_delete yes_delete