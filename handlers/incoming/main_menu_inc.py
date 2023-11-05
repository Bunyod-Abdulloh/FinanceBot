from aiogram import types
from aiogram.dispatcher import FSMContext

from handlers.all.all_functions import check_summary_main_inc
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

    await check_summary_main_inc(
        user_id=user_id,
        callback=call,
        section_name="📥 Kirim",
        total="📥 Kirim bo'limi uchun jami:",
        currency="so'm"
    )


# ========================== KIRIM > CATEGORY ==========================
@dp.callback_query_handler(text_contains="incoming_")
async def mmi_go_incoming_category(call: types.CallbackQuery):
    user_id = call.from_user.id
    incoming_name = call.data.split("_")[1]

    summary = await db.summary_category_inc(
        user_id=user_id,
        incoming_name=incoming_name
    )

    if summary is None:
        summary = 0

    await call.message.edit_text(
        text=f"<b>📥 Kirim > {incoming_name}</b>"
             f"\n\n{incoming_name} uchun jami kirim: <b>{summary}</b> so'm",
        reply_markup=await incoming_category(
            user_id=call.from_user.id,
            incoming_name=incoming_name
        )
    )
