from aiogram import types
from aiogram.dispatcher import FSMContext

from handlers.all.all_functions import replace_float
from keyboards.inline.incoming_keyboards import incoming_category
from keyboards.inline.out_in_keys import yes_again_buttons
from loader import dp, db
from states.user_states import IncomingCategory


# ========================== KIRIM CATEGORY > ==========================

# ADD SUMMARY
@dp.callback_query_handler(text_contains="addsummaryinc_", state="*")
async def ci_addsummary(call: types.CallbackQuery, state: FSMContext):
    incoming_name = call.data.split("_")[1]

    await state.update_data(
        incoming_name=incoming_name
    )
    await call.message.edit_text(
        text=f"<b>📥 Kirim > {incoming_name} > ➕ Summa qo'shish</b>"
             f"\n\nSummani kiriting:"
    )
    await IncomingCategory.add_summary.set()


@dp.message_handler(state=IncomingCategory.add_summary)
async def ci_check_summary(message: types.Message, state: FSMContext):
    data = await state.get_data()

    summary = await replace_float(
        message=message.text
    )
    await state.update_data(
        incoming_summary=summary
    )

    await message.answer(
        text=f"<b>📥 Kirim > {data['incoming_name']} > ➕ Summa qo'shish</b>"
             f"\n\nKirim nomi: {data['incoming_name']}"
             f"\nSumma: {summary} so'm"
             f"\n\nKiritilgan ma'lumotlarni tasdiqlaysizmi?",
        reply_markup=yes_again_buttons
    )
    await IncomingCategory.check_summary.set()


@dp.callback_query_handler(state=IncomingCategory.check_summary)
async def ci_check_summary(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()

    user_id = call.from_user.id
    incoming_name = data['incoming_name']
    summary = data['incoming_summary']

    if call.data == "yes":
        await db.add_incoming(
            user_id=user_id,
            incoming_name=incoming_name,
            summary=summary
        )

        summary_category = await db.summary_category_inc(
            user_id=user_id,
            incoming_name=incoming_name
        )

        await call.message.edit_text(
            text=f"<b>📥 Kirim > {incoming_name}</b>"
                 f"\n\nJami: <b>{summary_category}</b>",
            reply_markup=await incoming_category(
                user_id=user_id,
                incoming_name=incoming_name
            )
        )
        await call.answer(
            text="Kiritilgan ma'lumotlar saqlandi!",
            show_alert=True
        )
        await state.finish()

    elif call.data == "again":
        await call.message.edit_text(
            text=f"<b>📥 Kirim > {data['incoming_name']} > ➕ Summa qo'shish</b>"
                 f"\n\nSummani qayta kiriting:"
        )
        await IncomingCategory.add_summary.set()
