
# date_state = message.text
#     date_split = date_state.split('-')
#     date = datetime.date(year=int(date_split[0]),
#                          month=int(date_split[1]),
#                          day=int(date_split[2]))
#     await state.update_data(
#         date=date
#     )
#     data = await state.get_data()
#
#     await message.answer(
#         text=f'Category: <b>{data["category_name"]}</b>'
#              f'\nSubcategory: <b>{message.text}</b>'
#              f'\n\nMahsulot yoki harajat nomini kiriting:'
#     )

