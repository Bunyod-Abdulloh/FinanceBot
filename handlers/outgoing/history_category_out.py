import logging

from aiogram import types
from aiogram.dispatcher import FSMContext

from handlers.all.menu_handlers import navigate
from keyboards.inline.history_ikeys import PAGE_COUNT, buttons_generator
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
        text="Bosh menyu",
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
        user_id = call.from_user.id
        category = await db.get_categories_out(user_id=user_id)
        all_summary = await db.get_sum_all_out(user_id=user_id)

        if all_summary == 0:
            await call.answer(text=f"📤 Chiqim uchun to'lovlar mavjud emas!", show_alert=True)

        else:
            await call.message.delete()

            current_page = 1

            if len(category) % PAGE_COUNT == 0:
                all_pages = len(category) // PAGE_COUNT
            else:
                all_pages = len(category) // PAGE_COUNT + 1

            key = buttons_generator(current_page=current_page, all_pages=all_pages,
                                    subcategory="📤 Chiqim", category=True)
            history = " "

            for data in category[:PAGE_COUNT]:
                summary = await db.get_sum_category(user_id=user_id, category_name=data[0])
                history += f"{data[0]} | {summary} so'm\n"

            await call.message.answer(text=f"<b>📤 Chiqim > 📜 To'lovlar tarixi</b>"
                                           f"\n\n{history}\nJami: {all_summary} so'm",
                                      reply_markup=key)
            await state.update_data(
                current_page=current_page, all_pages=all_pages
            )
            history = " "
            await PayHistoryOut.category.set()
    except Exception as err:
        logging.error(err)


@dp.callback_query_handler(state=PayHistoryOut.category)
async def hs_handler(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()

    data = await state.get_data()

    current_page = data['current_page']
    all_pages = data['all_pages']
    if call.data == "prev":
        if current_page == 1:
            current_page = all_pages
        else:
            current_page -= 1
    if call.data == 'next':
        if current_page == all_pages:
            current_page = 1
        else:
            current_page += 1

    user_id = call.from_user.id
    category = await db.get_categories_out(user_id=user_id)
    all_summary = await db.get_sum_all_out(user_id=user_id)

    all_messages = category[(current_page - 1) * PAGE_COUNT: current_page * PAGE_COUNT]

    key = buttons_generator(current_page=current_page, all_pages=all_pages,
                            subcategory="📤 Chiqim", category=True)

    history = " "

    for data in all_messages:
        summary = await db.get_sum_category(user_id=user_id, category_name=data[0])
        history += f"{data[0]} | {summary} so'm\n"

    await call.message.answer(text=f"<b>📤 Chiqim > 📜 To'lovlar tarixi</b>"
                                   f"\n\n{history}\nJami: {all_summary} so'm",
                              reply_markup=key)
    history = " "
    await state.update_data(
        current_page=current_page, all_pages=all_pages)
