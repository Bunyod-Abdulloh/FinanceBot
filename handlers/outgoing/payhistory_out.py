import asyncio
import logging

from aiogram import types
from aiogram.dispatcher import FSMContext


from handlers.all.menu_handlers import navigate
# from handlers.all.sample import buttons_generator
from keyboards.inline.out_keyboards import buttons_generator
from loader import dp, db


@dp.callback_query_handler(text_contains="historycategory", state="*")
async def phout_category_history(call: types.CallbackQuery, state: FSMContext):
    print(call.data)


@dp.callback_query_handler(text_contains="historyproduct", state="*")
async def phout_product_history(call: types.CallbackQuery, state: FSMContext):
    try:
        subcategory_name = call.data.split("_")[1]
        date = await db.getdate_subcategory_out(user_id=call.from_user.id,
                                                subcategory_name=subcategory_name)

        if date:
            history = " "
            count = 0
            summary = 0

            for data in date[:50]:
                count += 1
                summary += data[1]
                history += f"{count}) {data[0]} | {data[1]} so'm\n"

            if len(date) < 50:
                key = buttons_generator(next_page=True)

                await call.message.edit_text(text=f"{history}\nJami: {summary} so'm",
                                             reply_markup=key)
            else:
                await state.update_data(summary=summary)

                key = buttons_generator(current_page=1, all_pages=2)

                await call.message.edit_text(text=f"{history}\nJami: {summary} so'm",
                                             reply_markup=key)

            history = " "

    except Exception as err:
        logging.error(err)


@dp.callback_query_handler(text="back_out", state="*")
async def pho_back_out(call: types.CallbackQuery, state: FSMContext):
    state_data = await state.get_data()

    await navigate(call=call,
                   callback_data=state_data,
                   state=state)
