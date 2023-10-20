import asyncio
import logging

from aiogram import types
from aiogram.dispatcher import FSMContext

from handlers.all.menu_handlers import navigate
from keyboards.inline.out_keyboards import back_out
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
        summary = await db.get_sum_subcategory(user_id=call.from_user.id,
                                               subcategory_name=subcategory_name)

        if date:
            state_data = await state.get_data()
            history = " "
            c = 0
            for data in date:
                c += 1
                history += f"{c}) {data[0]} | {data[1]} so'm\n"

                if len(history) == 4000:
                    await call.message.edit_text(text="To'lovlaringiz tarixi ko'pligi sababli sanalar oralig'ini "
                                                      "kiritishingizni so'raymiz!"
                                                      "Sanalar oralig'i quyidagi tartibda kiritilishi lozim:"
                                                      "\n\nYIL-OY-KUN ")
                    await navigate(call=call,
                                   callback_data=state_data,
                                   state=state)
                    await state.finish()
            await call.message.edit_text(text=f"{history}\nJami: {summary} so'm",
                                         reply_markup=back_out
                                         )
            history = " "
    except Exception as err:
        logging.error(err)


@dp.callback_query_handler(text="back_out", state="*")
async def pho_back_out(call: types.CallbackQuery, state: FSMContext):
    state_data = await state.get_data()

    await navigate(call=call,
                   callback_data=state_data,
                   state=state)
    # await state.finish()
