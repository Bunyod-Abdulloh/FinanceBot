from aiogram import types
from aiogram.dispatcher import FSMContext, filters

from handlers.all.all_functions import first_button_all_history_inc
from keyboards.inline.history_ikeys import PAGE_COUNT, buttons_generator
from loader import dp, db
from states.user_states import PayHistoryIncoming


@dp.callback_query_handler(text="historymain-inc", state="*")
async def mhi_history(call: types.CallbackQuery, state: FSMContext):
    user_id = call.from_user.id
    category = await db.get_userall_inc(user_id=user_id, distinct=True)
    all_summary = await db.summary_all_inc(user_id=user_id)

    if all_summary is None:
        await call.answer(text=f"Kirimlar mavjud emas!",
                          show_alert=True)
    else:
        await call.message.delete()
        await first_button_all_history_inc(
            current_page=1,
            database=category,
            call=call,
            state=state,
            back_name="📥 Kirim",
            currency="so'm",
            section_one="📥 Kirim",
            section_two="📜 Kirimlar tarixi",
            total="Kirim bo'limi uchun jami:",
            all_summary=all_summary
        )
        # await generate_history_button_one(
        #     two_columns=True,
        #     summary_inc=True,
        #     current_page=1,
        #     database=category,
        #     back_name="📥 Kirim",
        #     all_summary=all_summary,
        #     call=call,
        #     state=state,
        #     section_one="📥 Kirim",
        #     section_two="📜 Kirimlar tarixi",
        #     total="Jami",
        #     currency="so'm"
        # )
        await PayHistoryIncoming.category.set()


@dp.callback_query_handler(state=PayHistoryIncoming.category)
async def mhi_history_(call: types.CallbackQuery, state: FSMContext):

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

    user_id = call.from_user.id
    category = await db.get_userall_inc(user_id=user_id, distinct=True)
    all_summary = await db.summary_all_inc(user_id=user_id)

    all_messages = category[(current_page - 1) * PAGE_COUNT: current_page * PAGE_COUNT]

    key = buttons_generator(current_page=current_page, all_pages=all_pages,
                            incoming_main=True)

    history = " "

    for data in all_messages:
        summary = await db.summary_category_inc(user_id=user_id, incoming_name=data[0])
        history += f"{data[0]} | {summary} so'm\n"

    await call.message.answer(text=f"<b>📥 Kirim > 📜 Kirimlar tarixi</b>"
                                   f"\n\n{history}\n\n📥 Kirim bo'limi uchun jami: {all_summary} so'm",
                              reply_markup=key)
    history = " "
    await state.update_data(
        current_page=current_page, all_pages=all_pages)
