import asyncio
import logging

from aiogram import types
from aiogram.dispatcher import FSMContext

from handlers.all.all_functions import next_history_page
from handlers.all.menu_handlers import navigate
from handlers.all.sample import buttons_generator
from keyboards.inline.out_keyboards import back_out
from loader import dp, db


@dp.callback_query_handler(text_contains="historycategory", state="*")
async def phout_category_history(call: types.CallbackQuery, state: FSMContext):
    print(call.data)


@dp.callback_query_handler(text_contains="historyproduct", state="*")
async def phout_product_history(call: types.CallbackQuery, state: FSMContext):
    try:
        # all_messages = son  # db.get_all_message(_)
        #
        # # PEP8
        # if all_messages:
        #     current_page = 1
        #     # if len(all_messages) % 25 == 0 else
        #     if len(all_messages) % PAGE_COUNT == 0:
        #         all_pages = len(all_messages) // PAGE_COUNT
        #     else:
        #         all_pages = len(all_messages) // PAGE_COUNT + 1
        #     # 200 // 25
        #     key = buttons_generator(all_messages[:PAGE_COUNT], current_page=current_page, all_pages=all_pages)
        #     await message.answer(
        #         text="Ishlayapti",
        #         reply_markup=key
        #     )
        #     await state.update_data(
        #         current_page=current_page, all_pages=all_pages
        #     )
        #     await state.set_state("user_select_messages")
        # else:
        #     await message.answer(
        #         text="Xabarlar hozircha mavjud emas"
        #     )

        subcategory_name = call.data.split("_")[1]
        date = await db.getdate_subcategory_out(user_id=call.from_user.id,
                                                subcategory_name=subcategory_name)

        PAGE_COUNT = 50

        if date:
            h = " "
            c = 0
            s = 0

            for data in date[:PAGE_COUNT]:
                c += 1
                s += data[1]
                h += f"{c}) {data[0]} | {data[1]} so'm\n"

            if len(date) < 50:
                await call.message.edit_text(text=f"{h}\nJami: {s} so'm",
                                             reply_markup=back_out)
            else:
                key = buttons_generator(current_page=1, all_pages=2)
                await call.message.edit_text(text=f"{h}\nJami: {s} so'm",
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
    # await state.finish()
