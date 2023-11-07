import asyncio
import logging

from aiogram import types
from aiogram.dispatcher import FSMContext

from handlers.all.menu_handlers import navigate
from handlers.outgoing.functions_out import first_all_history_button_out, second_all_history_button_out
from keyboards.inline.out_in_keys import main_menu

from loader import dp, db
from states.user_states import PayHistoryOut


@dp.callback_query_handler(text="back_sub", state="*")
async def get_user_details(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()

    await navigate(call=call,
                   callback_data=data,
                   state=state)


@dp.callback_query_handler(text="back_category", state="*")
async def hc_back_category(call: types.CallbackQuery, state: FSMContext):
    await call.message.edit_text(
        text="<b>Bosh sahifa</b>",
        reply_markup=await main_menu()
    )
    await state.finish()


@dp.callback_query_handler(text_contains="pages", state="*")
async def hc_display_page(call: types.CallbackQuery):
    current_page = call.data.split("_")[1]
    await call.answer(text=f"Siz {current_page} - sahifadasiz!", show_alert=True)


@dp.callback_query_handler(text="historycategory", state="*")
async def hc_one(call: types.CallbackQuery, state: FSMContext):
    try:
        await call.message.delete()
        user_id = call.from_user.id
        database = await db.get_userall_out(
            user_id=user_id,
            distinct_category=True
        )
        all_summary = await db.get_summary_out(
            all_outgoing=True,
            user_id=user_id
        )
        if all_summary == 0:
            await call.answer(
                text=f"📤 Chiqimlar mavjud emas!",
                show_alert=True
            )
        await first_all_history_button_out(
            current_page=1,
            database=database,
            back_button="Bosh sahifa",
            call=call,
            language="uz_latin",
            state=state,
            currency="so`m",
            all_summary=all_summary,
            total="📤 Chiqim bo'limi",
            section_one="📤 Chiqim",
            section_two="📜 Chiqimlar tarixi"
        )
        await PayHistoryOut.category.set()
    except Exception as err:
        logging.error(err)


@dp.callback_query_handler(state=PayHistoryOut.category)
async def hs_handler(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()

    data = await state.get_data()
    current_page = data['current_page']
    all_pages = data['all_pages']
    database = await db.get_userall_out(
        user_id=call.from_user.id,
        distinct_category=True
    )
    all_summary = await db.get_summary_out(
        all_outgoing=True,
        user_id=call.from_user.id
    )
    await second_all_history_button_out(
        call=call,
        current_page=current_page,
        all_pages=all_pages,
        database=database,
        language="uz_latin",
        back_button="Bosh sahifa",
        currency="so`m",
        all_summary=all_summary,
        state=state,
        total="📤 Chiqim bo'limi",
        section_one="📤 Chiqim",
        section_two="📜 Chiqimlar tarixi"
    )
    