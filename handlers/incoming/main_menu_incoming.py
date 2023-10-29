from aiogram import types
from aiogram.dispatcher import FSMContext

from handlers.all.all_functions import warning_text, replace_point_bottom_line, raqam, replace_float
from keyboards.inline.incoming_keyboards import incoming_main_menu
from keyboards.inline.out_in_keys import yes_no_buttons, main_menu
from loader import dp, db
from states.user_states import IncomingStates


@dp.callback_query_handler(text="back_incomingmain", state="*")
async def incoming_back(call: types.CallbackQuery, state: FSMContext):
    await call.message.edit_text(
        text="Bosh menyu",
        reply_markup=await main_menu()
    )
    await state.finish()


@dp.callback_query_handler(text="incomingmenu", state="*")
async def incoming_main_(call: types.CallbackQuery):
    await call.message.edit_text(
        text="<b>📥 Kirim bo'limi</b>",
        reply_markup=await incoming_main_menu(
            user_id=call.from_user.id
        )
    )


@dp.callback_query_handler(text_contains="incoming_")
async def incoming_main_menu():
    pass
