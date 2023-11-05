from aiogram import types
from aiogram.dispatcher import FSMContext

from handlers.all.all_functions import generate_history_button_two, \
    first_category_history_button_inc
from keyboards.inline.incoming_keyboards import incoming_category
from loader import dp, db
from states.user_states import PayHistoryIncoming


@dp.callback_query_handler(text="back-inc-category", state="*")
async def chi_back_history_button(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()

    incoming_name = data['chi_incoming_name']

    await call.message.edit_text(
        text=f"<b>📥 Kirim > {incoming_name}</b>\n\n"
             f"{incoming_name} uchun jami kirim: {data['chi_summary_section']} so'm",
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
    summary_section = await db.summary_category_inc(user_id=user_id,
                                                    incoming_name=incoming_name)
    await state.update_data(
        chi_incoming_name=incoming_name,
        chi_summary_section=summary_section
    )
    await call.message.delete()
    await first_category_history_button_inc(
        current_page=1,
        back_button=incoming_name,
        database=incoming_db,
        currency="so'm",
        call=call,
        section_one="📥 Kirim",
        section_two="📜 Kirimlar tarixi",
        section_three=incoming_name,
        total=f"{incoming_name} uchun jami:",
        summary_section=summary_section,
        state=state
    )

    await PayHistoryIncoming.chi_one.set()


@dp.callback_query_handler(state=PayHistoryIncoming.chi_one)
async def chi_pay_history(call: types.CallbackQuery, state: FSMContext):

    await call.message.delete()

    data = await state.get_data()
    current_page = data['current_page']
    all_pages = data['all_pages']
    summary_section = data['chi_summary_section']
    incoming_name = data['chi_incoming_name']
    database = await db.get_user_inc(
        user_id=call.from_user.id,
        incoming_name=incoming_name
    )
    await generate_history_button_two(
        three_columns=True,
        call=call,
        current_page=current_page,
        all_pages=all_pages,
        back_name=incoming_name,
        database=database,
        section_one="📥 Kirim",
        section_two="📜 Kirimlar tarixi",
        section_three=incoming_name,
        currency="so'm",
        total="Jami",
        summary_section=summary_section,
        state=state,
        incoming_category=True
    )
