from aiogram import types
from aiogram.dispatcher import FSMContext

from handlers.all.all_functions import warning_text_uz_latin, warning_number_uz_latin
from keyboards.inline.incoming_keyboards import incoming_main_menu
from keyboards.inline.out_in_keys import yes_again_buttons
from loader import dp, db
from states.user_states import IncomingMainMenu


# ========================== ADD INCOMING ==============================
@dp.callback_query_handler(text="inc-add", state="*")
async def ih_add_incoming(call: types.CallbackQuery):
    await call.message.edit_text(
        text=f"<b>📥 Kirim</b>"
             f"\n\n{warning_text_uz_latin}"
             f"\n\nKirim uchun nom kiriting:"
    )
    await IncomingMainMenu.add_name.set()


@dp.message_handler(state=IncomingMainMenu.add_name)
async def ih_add_incoming_(message: types.Message, state: FSMContext):

    if message.text.isalpha():
        await state.update_data(
            ai_incoming_name=message.text
        )
        await message.answer(
            text=f"Summani kiriting:"
                 f"{warning_number_uz_latin}"
        )
        await IncomingMainMenu.add_summary.set()
    else:
        await message.answer(
            text=f"{warning_text_uz_latin}"
        )


@dp.message_handler(state=IncomingMainMenu.add_summary)
async def ih_add_summary(message: types.Message, state: FSMContext):
    data = await state.get_data()

    if message.text.isdigit():
        summary = int(message.text)
        await state.update_data(
            ai_incoming_summary=summary
        )

        await message.answer(
            text=f"Kirim nomi: <b>{data['ai_incoming_name']}</b>"
                 f"\nSumma: <b>{summary}</b> so`m"
                 f"\n\nKiritilgan ma'lumotlarni tasdiqlaysizmi?",
            reply_markup=yes_again_buttons
        )
        await IncomingMainMenu.add_check.set()
    else:
        await message.answer(
            text=f"{warning_number_uz_latin}"
        )


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

        await call.message.edit_text(
            text=f"<b>📥 Kirim bo'limi</b>"
                 f"\n\n📥 Kirim bo'limi uchun jami: {summary} so`m",
            reply_markup=await incoming_main_menu(
                user_id=user_id
            )
        )
        await state.finish()

    elif call.data == "again":

        await call.message.edit_text(
            text=f"<b>📥 Kirim</b>"
                 f"\n\n{warning_text_uz_latin}"
                 f"\n\nKirim uchun nom kiriting:"
        )
        await IncomingMainMenu.add_name.set()
