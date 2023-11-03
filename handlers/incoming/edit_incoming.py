from aiogram import types
from aiogram.dispatcher import FSMContext

from handlers.all.all_functions import warning_text_uz_latin, replace_point_bottom_line, replace_float
from keyboards.inline.out_in_keys import yes_again_buttons
from states.user_states import EditIncoming
from loader import dp, db


@dp.callback_query_handler(text_contains="editinc_", state="*")
async def ei_edit_incoming(call: types.CallbackQuery, state: FSMContext):
    incoming_name = call.data.split("_")[1]
    await state.update_data(
        ei_old_name=incoming_name
    )
    await call.message.edit_text(
        text=f"<b>📥 Kirim > {incoming_name}</b>"
             f"\n\n{warning_text_uz_latin}"
             f"\n\nYangi nom kiriting:"
    )
    await EditIncoming.add_name.set()


@dp.message_handler(state=EditIncoming.add_name)
async def ei_add_name_incoming(message: types.Message, state: FSMContext):

    new_name = await replace_point_bottom_line(message=message.text)
    await state.update_data(
        ei_new_name=new_name
    )
    data = await state.get_data()

    await message.answer(
        text=f"<b>📥 Kirim > {data['ei_old_name']}</b>"
             f"\n\nSummani kiriting:"
    )
    await EditIncoming.add_summary.set()


@dp.message_handler(state=EditIncoming.add_summary)
async def ei_add_summary(message: types.Message, state: FSMContext):

    summary = await replace_float(message=message.text)
    await state.update_data(
        ei_summary=summary
    )
    data = await state.get_data()

    await message.answer(
        text=f"<b>📥 Kirim > {data['ei_old_name']}</b>"
             f"\n\nKirim nomi: {data['ei_new_name']},"
             f"Summa: {summary}'] so'm"
             f"Kiritilgan ma'lumotlarni tasdiqlaysizmi?",
        reply_markup=yes_again_buttons
    )
    await EditIncoming.check.set()


@dp.callback_query_handler(state=EditIncoming.check)
async def ei_check_summary(call: types.CallbackQuery, state: FSMContext):

    data = await state.get_data()
    old_name = data['ei_old_name']
    new_name = data['ei_new_name']
    summary = data['ei_summary']
    user_id = call.from_user.id

    if call.data == "yes":
        await db.update_inc_name_and_summary(
            incoming_name=new_name,
            summary=summary,
            user_id=user_id
        )
        await call.message.edit_text(
            text=f"<b>📥 Kirim > {new_name}</b>",
        )

    elif call.data == "again":
        await call.message.edit_text(
            text=f"<b>📥 Kirim > {old_name}</b>"
                 f"\n\n{warning_text_uz_latin}"
                 f"\n\nQayta yangi nom kiriting:"
        )
        await EditIncoming.add_name.set()
