from aiogram import types
from aiogram.dispatcher import FSMContext

from handlers.incoming.function_inc import check_summary_main_inc
from keyboards.inline.incoming_keyboards import incoming_category
from keyboards.inline.out_in_keys import check_no_button
from loader import dp, db
from states.user_states import DeleteIncoming


@dp.callback_query_handler(text_contains="deleteinc_", state="*")
async def cdi_deleteinc(call: types.CallbackQuery, state: FSMContext):
    incoming_name = call.data.split("_")[1]
    await state.update_data(
        cdi_incoming_name=incoming_name
    )
    await call.message.edit_text(
        text=f"{incoming_name}ni o`chirishni istaysizmi?",
        reply_markup=check_no_button
    )
    await DeleteIncoming.delete_uz_latin.set()


@dp.callback_query_handler(state=DeleteIncoming.delete_uz_latin)
async def cdi_delete_uz_latin(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    user_id = call.from_user.id
    incoming_name = data['cdi_incoming_name']
    summary = await db.summary_category_inc(
        user_id=user_id,
        incoming_name=incoming_name
    )
    if call.data == "yes_delete":
        await db.delete_row_inc(
            user_id=user_id,
            incoming_name=incoming_name
        )
        await check_summary_main_inc(
            user_id=user_id,
            callback=call,
            section_name="📥 Kirim",
            total="📥 Kirim uchun jami:",
            currency="so`m"
        )
        await call.answer(
            text=f"{incoming_name} ma`lumotlari o`chirildi!",
            show_alert=True
        )

    if call.data == "no_delete":
        await call.message.edit_text(
            text=f"<b>📥 Kirim > {incoming_name}</b>"
                 f"\n\n{incoming_name} uchun jami kirim: {summary} so`m",
            reply_markup=await incoming_category(
                user_id=user_id,
                incoming_name=incoming_name
            )
        )
    await state.finish()
