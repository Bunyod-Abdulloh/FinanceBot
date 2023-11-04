from aiogram import types
from aiogram.dispatcher import FSMContext

from handlers.all.all_functions import generate_history_button_one, generate_history_button_two
from keyboards.inline.incoming_keyboards import incoming_category
from loader import dp, db
from states.user_states import PayHistoryIncoming


@dp.callback_query_handler(text="back-inc-category", state="*")
async def chi_back_history_button(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    incoming_name = data['chi_incoming_name']

    await call.message.edit_text(
        text=f"<b>📥 Kirim > {incoming_name}</b>\n\n"
             f"{incoming_name} uchun jami kirim: {data['chi_all_summary']} so'm",
        reply_markup=await incoming_category(user_id=call.from_user.id,
                                             incoming_name=incoming_name)
    )
    await state.finish()


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
    await state.update_data(
        chi_incoming_name=incoming_name,
        chi_all_summary=all_summary
    )

    await call.message.delete()
    await generate_history_button_one(current_page=1, database=incoming_db, back_name=incoming_name,
                                      all_summary=all_summary, call=call, state=state, section_one="📥 Kirim",
                                      section_two="📜 Kirimlar tarixi", section_three=incoming_name, total="Jami",
                                      currency="so'm", incoming_category=True)
    await PayHistoryIncoming.chi_one.set()


@dp.callback_query_handler(state=PayHistoryIncoming.chi_one)
async def chi_pay_history(call: types.CallbackQuery, state: FSMContext):

    await call.message.delete()

    data = await state.get_data()
    current_page = data['current_page']
    all_pages = data['all_pages']
    all_summary = data['chi_all_summary']
    incoming_name = data['chi_incoming_name']
    database = await db.get_user_inc(
        user_id=call.from_user.id,
        incoming_name=incoming_name
    )
    await generate_history_button_two(call=call, current_page=current_page, all_pages=all_pages,
                                      back_name=incoming_name, database=database, section_one="📥 Kirim",
                                      section_two="📜 Kirimlar tarixi", section_three=incoming_name, three_columns=True,
                                      currency="so'm", total="Jami", all_summary=all_summary, state=state,
                                      incoming_category=True)
