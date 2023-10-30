from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboards.inline.incoming_keyboards import incoming_main_menu, incoming_category
from keyboards.inline.out_in_keys import main_menu
from loader import dp, db


# ========================== < BUTTON BACK ==========================
@dp.callback_query_handler(text="back-main-menu", state="*")
async def incoming_back(call: types.CallbackQuery, state: FSMContext):
    await call.message.edit_text(
        text="Bosh menyu",
        reply_markup=await main_menu()
    )
    await state.finish()


# ========================== BUTTON KIRIM ==========================
@dp.callback_query_handler(text="incomingmenu", state="*")
async def incoming_main_(call: types.CallbackQuery):
    user_id = call.from_user.id

    all_summary = await db.summary_all_inc(
        user_id=user_id
    )

    if all_summary is None:
        all_summary = 0

    await call.message.edit_text(
        text=f"<b>📥 Kirim bo'limi</b>"
             f"\n\nJami: <b>{all_summary}</b> so'm",
        reply_markup=await incoming_main_menu(
            user_id=user_id
        )
    )


# ========================== KIRIM > ==========================
@dp.callback_query_handler(text_contains="incoming_")
async def mmi_go_incoming_category(call: types.CallbackQuery):
    user_id = call.from_user.id
    incoming_name = call.data.split("_")[1]
    summary = await db.summary_category_inc(
        user_id=user_id,
        incoming_name=incoming_name
    )

    await call.message.edit_text(
        text=f"<b>📥 Kirim > {incoming_name}</b>"
             f"\n\nJami: <b>{summary}</b> so'm",
        reply_markup=await incoming_category(
            user_id=call.from_user.id,
            incoming_name=incoming_name
        )
    )
