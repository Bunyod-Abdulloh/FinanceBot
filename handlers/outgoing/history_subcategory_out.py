import logging

from aiogram import types
from aiogram.dispatcher import FSMContext

from handlers.outgoing.functions_out import first_all_history_button_out, first_category_history_button_out
from keyboards.inline.history_ikeys import PAGE_COUNT, buttons_generator
from loader import dp, db
from states.user_states import PayHistoryOut


@dp.callback_query_handler(text_contains="historysub", state="*")
async def historysub_out(call: types.CallbackQuery, state: FSMContext):

    category = call.data.split("_")[1]
    user_id = call.from_user.id

    database = await db.get_subcategory_out(
        distinct_subcategory=True,
        category_name=category,
        user_id=user_id
    )
    category_summary = await db.get_summary_out(
        category=True,
        user_id=user_id,
        category_name=category
    )
    if category_summary == 0:
        await call.answer(text=f"{category} uchun to'lovlar mavjud emas!", show_alert=True)

    else:
        await call.message.delete()
        await first_category_history_button_out(
            current_page=1,
            database=database,
            language="uz_latin",
            currency="so`m",
            call=call,
            total=category,
            section_summary=category_summary,
            state=state,
            section_one="📤 Chiqim",
            section_two=category,
            section_three="📜 Bo`lim hisoboti"
        )


@dp.callback_query_handler(state=PayHistoryOut.subcategory)
async def sh_message_handler(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()

    data = await state.get_data()

    current_page = data['current_page']
    all_pages = data['all_pages']
    if call.data == "prev":
        if current_page == 1:
            current_page = all_pages
        else:
            current_page -= 1
    if call.data == 'next':
        if current_page == all_pages:
            current_page = 1
        else:
            current_page += 1

    category = data["category"]
    user_id = call.from_user.id
    subcategory = await db.getdate_category_out(category_name=category, user_id=user_id)
    category_summary = await db.get_sum_category(user_id=user_id, category_name=category)

    all_messages = subcategory[(current_page - 1) * PAGE_COUNT: current_page * PAGE_COUNT]

    key = buttons_generator(current_page, all_pages, category)

    history = " "

    for data in all_messages:
        summary = await db.get_sum_subcategory(user_id=user_id, subcategory_name=data[0])
        history += f"{data[0]} | {summary} so'm\n"

    await call.message.answer(text=f"<b>📤 Chiqim > {category} > 📜 To'lovlar tarixi</b>"
                                   f"\n\n{history}\nJami: {category_summary} so'm",
                              reply_markup=key)
    history = " "
    await state.update_data(
        current_page=current_page, all_pages=all_pages
    )
