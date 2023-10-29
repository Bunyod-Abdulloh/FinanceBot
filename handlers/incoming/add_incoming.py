from aiogram import types
from aiogram.dispatcher import FSMContext

from handlers.all.all_functions import replace_point_bottom_line, warning_text, raqam, replace_float
from keyboards.inline.incoming_keyboards import incoming_main_menu
from keyboards.inline.out_in_keys import yes_no_buttons
from loader import dp, db
from states.user_states import IncomingStates


# ========================== ADD INCOMING ==============================
@dp.callback_query_handler(text="incoming_add", state="*")
async def ih_add_incoming(call: types.CallbackQuery):
    await call.message.edit_text(
        text=f"<b>📥 Kirim</b>"
             f"\n\n{warning_text}"
             f"\n\nKirim uchun nom kiriting:"
    )
    await IncomingStates.add_name.set()


@dp.message_handler(state=IncomingStates.add_name)
async def ih_add_incoming_(message: types.Message, state: FSMContext):

    message_ = await replace_point_bottom_line(message=message.text)
    await state.update_data(
        incoming_name=message_
    )
    await message.answer(
        text=f"Summani kiriting"
             f"{raqam}"
    )
    await IncomingStates.add_summary.set()


@dp.message_handler(state=IncomingStates.add_summary)
async def ih_add_summary(message: types.Message, state: FSMContext):
    data = await state.get_data()

    summary = await replace_float(message=message.text)

    await state.update_data(
        incoming_summary=summary
    )

    await message.answer(
        text=f"Kirim nomi: <b>{data['incoming_name']}</b>"
             f"\nSumma: <b>{summary}</b>"
             f"\n\nKiritilgan ma'lumotlarni tasdiqlaysizmi?",
        reply_markup=yes_no_buttons
    )
    await IncomingStates.add_check.set()


@dp.callback_query_handler(state=IncomingStates.add_check)
async def ih_add_check(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()

    if call.data == "yes_button":

        await db.add_incoming(user_id=call.from_user.id,
                              incoming_name=data['incoming_name'],
                              summary=data['incoming_summary'])

        await call.answer(
            text="Ma'lumotlar tasdiqlandi!",
            show_alert=True
        )

        await call.message.edit_text(
            text="<b>📥 Kirim bo'limi</b>",
            reply_markup=await incoming_main_menu(
                user_id=call.from_user.id
            )
        )
        await state.finish()

    elif call.data == "again_button":

        await call.message.edit_text(
            text=f"<b>📥 Kirim</b>"
                 f"\n\n{warning_text}"
                 f"\n\nKirim uchun nom kiriting:"
        )
        await IncomingStates.add_name.set()
