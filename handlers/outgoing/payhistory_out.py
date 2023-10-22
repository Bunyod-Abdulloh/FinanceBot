import logging

from aiogram import types
from aiogram.dispatcher import FSMContext

from handlers.all.menu_handlers import navigate
from keyboards.inline.out_keyboards import buttons_generator

from loader import dp, db
from states.user_states import PayHistoryOut


@dp.callback_query_handler(text_contains="historycategory", state="*")
async def phout_category_history(call: types.CallbackQuery, state: FSMContext):
    print(call.data)


@dp.callback_query_handler(text_contains="historyproduct", state="*")
async def phout_product_history(call: types.CallbackQuery, state: FSMContext):
    try:
        subcategory_name = call.data.split("_")[1]
        get_data = await db.getdate_subcategory_out(user_id=call.from_user.id,
                                                    subcategory_name=subcategory_name)
        summary = await db.get_sum_subcategory(user_id=call.from_user.id,
                                               subcategory_name=subcategory_name)
        if get_data:
            history = " "
            count = 0

            for data in get_data[:2]:
                count += 1
                history += f"{count}) {data[0]} | {data[1]} so'm\n"

            if len(get_data) < 2:
                key = buttons_generator(next_page=True)

                await call.message.edit_text(text=f"{history}\nJami: {summary} so'm",
                                             reply_markup=key)
            else:
                key = buttons_generator(current_page=1, all_pages=2)

                await call.message.edit_text(text=f"{history}\nJami: {summary} so'm",
                                             reply_markup=key)
            history = " "
            await PayHistoryOut.one.set()

    except Exception as err:
        logging.error(err)


@dp.callback_query_handler(state=PayHistoryOut.one)
async def pho_back_out(call: types.CallbackQuery, state: FSMContext):
    state_data = await state.get_data()

    if call.data == "back_out":
        await navigate(call=call,
                       callback_data=state_data,
                       state=state)

    elif call.data == "next":
        subcategory = state_data["subcategory"]
        summary = await db.get_sum_subcategory(user_id=call.from_user.id,
                                               subcategory_name=subcategory)

        get_data = await db.getdate_subcategory_out(user_id=call.from_user.id,
                                                    subcategory_name=subcategory)

        history = " "
        count = 50

        for data in get_data[2:]:
            count += 1
            history += f"{count}) {data[0]} | {data[1]} so'm\n"

        key = buttons_generator(prev_page=True)
        await call.message.edit_text(text=f"{history}\nJami: {summary} so'm",
                                     reply_markup=key)
        await PayHistoryOut.two.set()


@dp.callback_query_handler(text="prev_out", state=PayHistoryOut.two)
async def phout_prev(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    user_id = call.from_user.id
    subcategory = data["subcategory"]
    summary = await db.get_sum_subcategory(user_id=user_id,
                                           subcategory_name=subcategory)
    get_data = await db.getdate_subcategory_out(user_id=user_id,
                                                subcategory_name=subcategory)

    history = " "
    count = 0

    for data in get_data[:2]:
        count += 1
        history += f"{count}) {data[0]} | {data[1]} so'm\n"

    if len(get_data) < 2:
        key = buttons_generator(next_page=True)

        await call.message.edit_text(text=f"{history}\nJami: {summary} so'm",
                                     reply_markup=key)
    else:
        await state.update_data(summary=summary)

        key = buttons_generator(current_page=1, all_pages=2)

        await call.message.edit_text(text=f"{history}\nJami: {summary} so'm",
                                     reply_markup=key)
    history = " "
    await PayHistoryOut.one.set()
