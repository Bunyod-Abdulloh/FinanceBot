from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from loader import dp, db
from aiogram import types

from states.user_states import PayHistoryOut


PAGE_COUNT = 50


def buttons_generator(current_page: int, all_pages: int, subcategory: str):
    key = InlineKeyboardMarkup(
        row_width=3
    )
    key.add(
        InlineKeyboardButton(
            text="⬅️ Ortga",
            callback_data="prev"
        ))

    key.insert(
        InlineKeyboardButton(
            text=f"{current_page}/{all_pages}",
            callback_data="pages"
        )
    )

    key.insert(InlineKeyboardButton(
        text="Oldinga ➡️",
        callback_data="next"
    )
    )
    key.add(InlineKeyboardButton(
        text=f"↩️ {subcategory}ga qaytish",
        callback_data="back_sub"
    ))
    return key


@dp.callback_query_handler(text_contains="historyproduct", state="*")
async def sasasample(call: types.CallbackQuery, state: FSMContext):
    subcategory_name = call.data.split("_")[1]
    get_data = await db.getdate_subcategory_out(user_id=call.from_user.id,
                                                subcategory_name=subcategory_name)
    summary = await db.get_sum_subcategory(user_id=call.from_user.id,
                                           subcategory_name=subcategory_name)
    if summary == 0:
        await call.answer(text=f"{subcategory_name} uchun to'lovlar mavjud emas!", show_alert=True)

    else:

        current_page = 1

        if len(get_data) % PAGE_COUNT == 0:
            all_pages = len(get_data) // PAGE_COUNT
        else:
            all_pages = len(get_data) // PAGE_COUNT + 1
        # 200 // 25
        key = buttons_generator(current_page=current_page, all_pages=all_pages,
                                subcategory=subcategory_name)
        history = " "

        for data in get_data[:PAGE_COUNT]:
            history += f"{data[0]} | {data[1]} so'm\n"

        await call.message.answer(text=f"{history}\nJami: {summary} so'm",
                                  reply_markup=key)
        await state.update_data(
            current_page=current_page, all_pages=all_pages
        )
        history = " "
        await PayHistoryOut.one.set()


@dp.callback_query_handler(state="user_select_messages", text_contains="message_")
async def get_user_details(call: types.CallbackQuery, state: FSMContext):
    await call.answer(
        text=f"You are selected {call.data.split('_')[1]} number",
        show_alert=True
    )


@dp.callback_query_handler(state=PayHistoryOut.one)
async def select_message_handler(call: types.CallbackQuery, state: FSMContext):
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

    subcategory = data["subcategory"]
    user_id = call.from_user.id
    get_data = await db.getdate_subcategory_out(user_id=user_id,
                                                subcategory_name=subcategory)
    summary = await db.get_sum_subcategory(user_id=user_id,
                                           subcategory_name=subcategory)
    all_messages = get_data[(current_page - 1) * PAGE_COUNT: current_page * PAGE_COUNT]

    key = buttons_generator(current_page, all_pages, subcategory)

    history = " "

    for data in all_messages:
        history += f"{data[0]} | {data[1]} so'm\n"

    await call.message.answer(text=f"{history}\nJami: {summary} so'm",
                              reply_markup=key)
    history = " "
    await state.update_data(
        current_page=current_page, all_pages=all_pages
    )
