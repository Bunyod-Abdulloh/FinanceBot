from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboards.inline.history_ikeys import PAGE_COUNT, buttons_generator
from keyboards.inline.out_in_keys import back_history_inc_button
from loader import dp, db


@dp.callback_query_handler(text="back-history-inc", state="*")
async def chi_back_history_button(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    print(data)
    await state.finish()
    # await call.message.edit_text(
    #     text=""
    # )


@dp.callback_query_handler(text_contains="historycategoryinc_", state="*")
async def chi_history(call: types.CallbackQuery, state: FSMContext):
    incoming_name = call.data.split("_")[1]
    user_id = call.from_user.id

    incoming_db = await db.get_user_inc(
        user_id=user_id,
        incoming_name=incoming_name
    )

    all_summary = await db.summary_category_inc(user_id=user_id,
                                                incoming_name=incoming_name)

    await call.message.delete()
    current_page = 1

    if len(incoming_db) % PAGE_COUNT == 0:
        all_pages = len(incoming_db) // PAGE_COUNT
    else:
        all_pages = len(incoming_db) // PAGE_COUNT + 1

    key = buttons_generator(current_page=current_page, all_pages=all_pages,
                            subcategory=incoming_name)

    history = " "

    for n in incoming_db:
        history += f"{n[2]} | {n[0]} | {n[1]} so'm\n"

    await call.message.edit_text(
        text=f"<b>📥 Kirim > 📜 Kirimlar tarixi</b>"
             f"\n\n{history}\n\nJami: {all_summary} so'm",
        reply_markup=back_history_inc_button
    )
