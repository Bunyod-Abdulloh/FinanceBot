import asyncio

from aiogram import types
from aiogram.dispatcher import FSMContext

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
            history = " "
            if len(history) == 4000:
                await call.message.edit_text(text="To'lovlaringiz tarixi ko'pligi sababli sanalar oralig'ini "
                                                  "kiritishingizni so'raymiz!"
                                                  "Sanalar oralig'i quyidagi tartibda kiritilishi lozim:"
                                                  "\n\nYIL-OY-KUN ")
            for data in date:
                history += f"{data[0]} | {data[1]} so'm\n"
            #
            #     await db.add_history(user_id=call.from_user.id,
            #                          history=f" | {data[1]} so'm",
            #                          subcategory_name=subcategory_name
            #                          )
            #     await asyncio.sleep(3)
            #
            # history = await db.get_history(user_id=call.from_user.id,
            #                                subcategory_name=subcategory_name)
            await call.message.edit_text(text=f"{history}\n<b>Jami: {summary} so'm</b>")

            print(len(history))

    except Exception as err:
        print(err)

