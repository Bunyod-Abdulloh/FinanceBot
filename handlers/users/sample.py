# from aiogram.dispatcher import FSMContext
# from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
# from loader import dp
# from aiogram import types
#
# son = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
#
# PAGE_COUNT = 25
#
#
# @dp.message_handler(text='Xabarlar', state='*')
# async def sasasample(message: types.Message, state: FSMContext):
#     all_messages = son  # db.get_all_message(_)
#
#     # PEP8
#     if all_messages:
#         current_page = 1
#         # if len(all_messages) % 25 == 0 else
#         if len(all_messages) % PAGE_COUNT == 0:
#             all_pages = len(all_messages) // PAGE_COUNT
#         else:
#             all_pages = len(all_messages) // PAGE_COUNT + 1
#         # 200 // 25
#         key = buttons_generator(database=all_messages[:PAGE_COUNT],
#                                 current_page=current_page,
#                                 all_pages=all_pages)
#         await message.answer(
#             text="Ishlayapti",
#             reply_markup=key
#         )
#         await state.update_data(
#             current_page=current_page,
#             all_pages=all_pages
#         )
#         await state.set_state("user_select_messages")
#     else:
#         await message.answer(
#             text="Xabarlar hozircha mavjud emas"
#         )
#
#
# @dp.callback_query_handler(state="user_select_messages", text_contains="message_")
# async def get_user_details(call: types.CallbackQuery, state: FSMContext):
#     await call.answer(
#         text=f"You are selected {call.data.split('_')[1]} number",
#         show_alert=True
#     )
#
#
# @dp.callback_query_handler(state="user_select_messages")
# async def select_message_handler(call: types.CallbackQuery, state: FSMContext):
#     data = await state.get_data()
#     await call.message.delete()
#     call_data = call.data
#     current_page = data['current_page']
#     all_pages = data['all_pages']
#     if call.data == "prev":
#         if current_page == 1:
#             current_page = all_pages
#         else:
#             current_page -= 1
#     if call.data == 'next':
#         if current_page == all_pages:
#             current_page = 1
#         else:
#             current_page += 1
#
#     all_messages = son[(current_page - 1) * PAGE_COUNT: current_page * PAGE_COUNT]
#
#     key = buttons_generator(all_messages, current_page, all_pages)
#     await call.message.answer(
#         text="Ishlayapti",
#         reply_markup=key
#     )
#     await state.update_data(
#         current_page=current_page, all_pages=all_pages
#     )