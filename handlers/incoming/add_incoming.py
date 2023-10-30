from aiogram import types
from aiogram.dispatcher import FSMContext

from handlers.all.all_functions import replace_point_bottom_line, warning_text, raqam, replace_float
from keyboards.inline.incoming_keyboards import incoming_main_menu
from keyboards.inline.out_in_keys import yes_again_buttons
from loader import dp, db
from states.user_states import IncomingMainMenu


# ========================== ADD INCOMING ==============================
@dp.callback_query_handler(text="inc-add", state="*")
async def ih_add_incoming(call: types.CallbackQuery):
    await call.message.edit_text(
        text=f"<b>📥 Kirim</b>"
             f"\n\n{warning_text}"
             f"\n\nKirim uchun nom kiriting:"
    )
    await IncomingMainMenu.add_name.set()


@dp.message_handler(state=IncomingMainMenu.add_name)
async def ih_add_incoming_(message: types.Message, state: FSMContext):

    message_ = await replace_point_bottom_line(message=message.text)
    await state.update_data(
        ai_incoming_name=message_
    )
    await message.answer(
        text=f"Summani kiriting"
             f"{raqam}"
    )
    await IncomingMainMenu.add_summary.set()


@dp.message_handler(state=IncomingMainMenu.add_summary)
async def ih_add_summary(message: types.Message, state: FSMContext):
    data = await state.get_data()

    summary = await replace_float(message=message.text)

    await state.update_data(
        ai_incoming_summary=summary
    )

    await message.answer(
        text=f"Kirim nomi: <b>{data['ai_incoming_name']}</b>"
             f"\nSumma: <b>{summary}</b> so'm"
             f"\n\nKiritilgan ma'lumotlarni tasdiqlaysizmi?",
        reply_markup=yes_again_buttons
    )
    await IncomingMainMenu.add_check.set()


@dp.callback_query_handler(state=IncomingMainMenu.add_check)
async def ih_add_check(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    user_id = call.from_user.id

    if call.data == "yes":

        await db.add_incoming(user_id=user_id,
                              incoming_name=data['ai_incoming_name'],
                              summary=data['ai_incoming_summary'])

        await call.answer(
            text="Kiritilgan ma'lumotlar saqlandi!",
            show_alert=True
        )
        
        summary = await db.summary_all_inc(user_id=user_id)
        if summary is None:
            summary = 0

        await call.message.edit_text(
            text=f"<b>📥 Kirim bo'limi</b>"
                 f"\n\n📥 Kirim bo'limi uchun jami: {summary} so'm",
            reply_markup=await incoming_main_menu(
                user_id=user_id
            )
        )
        await state.finish()

    elif call.data == "again":

        await call.message.edit_text(
            text=f"<b>📥 Kirim</b>"
                 f"\n\n{warning_text}"
                 f"\n\nKirim uchun nom kiriting:"
        )
        await IncomingMainMenu.add_name.set()
