import logging

from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboards.inline.history_ikeys import PAGE_COUNT, buttons_generator
from loader import dp, db
from states.user_states import PayHistoryIncoming


@dp.callback_query_handler(text="historymain-inc", state="*")
async def mhi_history(call: types.CallbackQuery, state: FSMContext):
    user_id = call.from_user.id
    category = await db.get_userall_inc(user_id=user_id, distinct=True)
    all_summary = await db.summary_all_inc(user_id=user_id)
    try:
        if all_summary is None:
            await call.answer(text=f"Kirimlar uchun mavjud emas!",
                              show_alert=True)
        else:
            await call.message.delete()

            current_page = 1

            if len(category) % PAGE_COUNT == 0:
                all_pages = len(category) // PAGE_COUNT
            else:
                all_pages = len(category) // PAGE_COUNT + 1

            key = buttons_generator(current_page=current_page, all_pages=all_pages,
                                    incoming_main=True)
            history = " "

            for data in category[:PAGE_COUNT]:
                summary = await db.summary_category_inc(user_id=user_id, incoming_name=data[0])
                history += f"{data[0]} | {summary} so'm\n"

            await call.message.answer(text=f"<b>📥 Kirim > 📜 Kirimlar tarixi</b>"
                                           f"\n\n{history}\n\n📥 Kirim bo'limi uchun jami: {all_summary} so'm",
                                      reply_markup=key)
            await state.update_data(
                current_page=current_page, all_pages=all_pages
            )
            history = " "
            await PayHistoryIncoming.category.set()

    except Exception as err:\
        logging.error(err)


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
