from aiogram import types
from aiogram.dispatcher import FSMContext

from handlers.all.all_functions import generate_history_button
from keyboards.inline.history_ikeys import PAGE_COUNT, buttons_generator
from keyboards.inline.out_in_keys import back_history_inc_button
from loader import dp, db
from states.user_states import PayHistoryIncoming


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

    await generate_history_button(current_page=1, database=incoming_db, back_name=incoming_name,
                                  all_summary=all_summary, call=call, state=state,
                                  section="📥 Kirim", history_name="📜 Kirimlar tarixi",
                                  total="Jami", currency="so'm")

    await PayHistoryIncoming.chi_one.set()


@dp.callback_query_handler(state=PayHistoryIncoming.chi_one):
async def chi_pay_history(call: types.CallbackQuery, state: FSMContext):

    await call.message.delete()




