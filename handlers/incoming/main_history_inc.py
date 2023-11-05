from aiogram import types
from aiogram.dispatcher import FSMContext

from handlers.incoming.function_inc import first_all_history_button_inc, second_all_history_button_inc
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
        await first_all_history_button_inc(
            current_page=1,
            database=category,
            call=call,
            language="uz_latin",
            state=state,
            back_button="📥 Kirim",
            currency="so'm",
            all_summary=all_summary
        )
        await PayHistoryIncoming.category.set()


@dp.callback_query_handler(state=PayHistoryIncoming.category)
async def mhi_history_(call: types.CallbackQuery, state: FSMContext):

    await call.message.delete()
    data = await state.get_data()

    current_page = data['current_page']
    all_pages = data['all_pages']
    category = await db.get_userall_inc(
        user_id=call.from_user.id,
        distinct=True
    )
    all_summary = await db.summary_all_inc(
        user_id=call.from_user.id
    )
    await second_all_history_button_inc(
        call=call,
        language="uz_latin",
        current_page=current_page,
        all_pages=all_pages,
        database=category,
        back_button="📥 Kirim",
        currency="so'm",
        all_summary=all_summary,
        state=state
    )
