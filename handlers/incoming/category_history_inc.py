from aiogram import types
from aiogram.dispatcher import FSMContext

from handlers.incoming.function_inc import first_category_history_button_inc, second_category_history_button_inc
from keyboards.inline.incoming_keyboards import incoming_category
from loader import dp, db
from states.user_states import PayHistoryIncoming


@dp.message_handler(text="ada", state="*")
async def sampleada(message: types.Message):
    h = await db.get_userall_inc(user_id=message.from_user.id)
    print(h)


@dp.callback_query_handler(text="back-inc-category", state="*")
async def chi_back_history_button(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()

    incoming_name = data['chi_incoming_name']

    await call.message.edit_text(
        text=f"<b>📥 Kirim > {incoming_name}</b>\n\n"
             f"{incoming_name} uchun jami kirim: {data['chi_summary_section']} so`m",
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
    section_summary = await db.summary_category_inc(user_id=user_id,
                                                    incoming_name=incoming_name)
    await state.update_data(
        chi_incoming_name=incoming_name,
        chi_summary_section=section_summary
    )
    await call.message.delete()
    await first_category_history_button_inc(
        current_page=1,
        database=incoming_db,
        language="uz_latin",
        currency="so`m",
        call=call,
        section_name=incoming_name,
        section_summary=section_summary,
        state=state
    )
    await PayHistoryIncoming.chi_one.set()


def second_category_history_buttons_inc():
    pass


@dp.callback_query_handler(state=PayHistoryIncoming.chi_one)
async def chi_pay_history(call: types.CallbackQuery, state: FSMContext):

    await call.message.delete()

    data = await state.get_data()
    current_page = data['current_page']
    all_pages = data['all_pages']
    section_summary = data['chi_summary_section']
    incoming_name = data['chi_incoming_name']

    database = await db.get_user_inc(
        user_id=call.from_user.id,
        incoming_name=incoming_name
    )

    await second_category_history_button_inc(
        call=call,
        current_page=current_page,
        all_pages=all_pages,
        database=database,
        section_name=incoming_name,
        section_summary=section_summary,
        currency="so`m",
        language="uz_latin",
        state=state
    )
