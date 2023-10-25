from aiogram import types
from aiogram.dispatcher import FSMContext

from handlers.all.all_functions import warning_text, replace_point_bottom_line, raqam, replace_float
from keyboards.inline.incoming_keyboards import incoming_main_menu
from loader import dp, db
from states.user_states import IncomingStates


@dp.callback_query_handler(text="incoming", state="*")
async def incoming_main_(call: types.CallbackQuery):
    await call.message.edit_text(
        text="<b>📥 Kirim bo'limi</b>",
        reply_markup=await incoming_main_menu(
            user_id=call.from_user.id
        )
    )


@dp.callback_query_handler(text="incoming_add", state="*")
async def ih_add_incoming(call: types.CallbackQuery, state: FSMContext):
    await call.message.edit_text(
        text=f"<b>📥 Kirim</b>"
             f"\n\nKirim uchun nom kiriting"
             f"\n{warning_text}"
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
        text=f""
             f"Kiritilgan ma'lumotlarni tasdiqlaysizmi?"
    )

