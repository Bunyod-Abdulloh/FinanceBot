from aiogram import types
from aiogram.dispatcher import FSMContext

from handlers.all.all_functions import replace_function, replace_point, replace_float
from keyboards.default.start_keyboard import menu
from keyboards.inline.out_keyboards import categories_keyboard, yes_no_buttons
from loader import dp, db
from states.user_states import FinanceCategory


digits = "\n(faqat raqam kiritilishi lozim!):"


@dp.callback_query_handler(text='add_category', state='*')
async def add_category_call(call: types.CallbackQuery):
    await call.message.delete()

    await call.message.answer(
        text=f"Bo'lim: <b>📤 Chiqim</b>"
             f"\n\nKategoriya nomini kiriting:",
        reply_markup=menu
    )
    await FinanceCategory.add_category.set()


@dp.message_handler(state=FinanceCategory.add_category)
async def add_category(message: types.Message, state: FSMContext):

    category_name = await replace_point(message=message.text)

    await state.update_data(
        category_name=category_name
    )

    await message.answer(
        text=f"Bo'lim: <b>📤 Chiqim</b>"
             f"\nKategoriya: <b>{category_name}</b>"
             f"\n\nSubkategoriya nomini kiriting:"
    )
    await FinanceCategory.add_subcategory.set()


@dp.message_handler(state=FinanceCategory.add_subcategory)
async def add_subcategory_out(message: types.Message, state: FSMContext):

    subcategory_name = await replace_point(message=message.text)

    await state.update_data(
        subcategory_name=subcategory_name
    )

    data = await state.get_data()

    await message.answer(
        text=f"Bo'lim: <b>📤 Chiqim</b>"
             f"\nKategoriya: <b>{data['category_name']}</b>"
             f"\nSubkategoriya: <b>{message.text}</b>"
             f"\n\nHarajat summasini kiriting"
             f"{digits}"
    )
    await FinanceCategory.summary.set()


@dp.message_handler(state=FinanceCategory.summary)
async def all_users_out(message: types.Message, state: FSMContext):

    summary = await replace_float(message=message.text)

    data = await state.get_data()

    await state.update_data(
        summary=int(summary)
    )

    await message.answer(
        text=f"Bo'lim: <b>📤 Chiqim</b>"
             f"\nKategoriya: <b>{data['category_name']}</b>"
             f"\nSubkategoriya: <b>{data['subcategory_name']}</b>"
             f"\nHarajat summasi: <b>{summary}</b>"
             f"\n\nKiritilgan ma'lumotlarni tasdiqlaysizmi?",
        reply_markup=yes_no_buttons
    )
    await FinanceCategory.summary_check.set()


@dp.callback_query_handler(state=FinanceCategory.summary_check)
async def all_users_check_out(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()

    user_id = call.from_user.id
    category_name = data['category_name']
    subcategory_name = data['subcategory_name']
    summary = data['summary']

    if call.data == "yes_button":
        await db.first_add_out(
            user_id=user_id,
            category_name=category_name,
            subcategory_name=subcategory_name,
            summary=summary
        )
        await call.message.edit_text(
            text="Harajat bazaga qo'shildi!",
            reply_markup=await categories_keyboard(user_id=user_id)
        )
        await state.finish()

    elif call.data == "again_button":
        await call.message.edit_text(
            text=f"Bo'lim: <b>📤 Chiqim</b>"
                 f"\n\nKategoriya nomini kiriting:")
        await FinanceCategory.add_category.set()


# @dp.message_handler(state=FinanceCategory.add_product)
# async def add_product(message: types.Message, state: FSMContext):
#     await state.update_data(
#         product_name=message.text
#     )
#
#     data = await state.get_data()
#
#     await message.answer(
#         text=f"Kategoriya: <b>{data['category_name']}</b>"
#              f"\nSubkategoriya: <b>{data['subcategory_name']}</b>"
#              f"\nMahsulot nomi: <b>{message.text}</b>"
#              f"\n\nMahsulot soni yoki vaznini kiriting"
#              f"{digits}",
#         reply_markup=summary_or_item_keyboard()
#     )
#     await FinanceCategory.summary_or_item.set()
#
#
# @dp.callback_query_handler(state=FinanceCategory.summary_or_item)
# async def summary_or_item(call: types.CallbackQuery, state: FSMContext):
#     await call.message.delete()
#
#     data = await state.get_data()
#     text = (f"Kategoriya: <b>{data['category_name']}</b>"
#             f"\nSubkategoriya: <b>{data['subcategory_name']}</b>"
#             f"\nMahsulot nomi: <b>{data['product_name']}</b>")
#
#     if call.data == 'item':
#         await call.message.answer(
#             text=f'{text}'
#                  f"\n\nMahsulot sonini kiriting"
#                  f"{digits}"
#         )
#         await FinanceCategory.item.set()
#
#     elif call.data == 'item_kg':
#         await call.message.answer(
#             text=f'{text}'
#                  f"\n\nMahsulot vaznini kiriting:"
#                  f"{digits}"
#         )
#         await FinanceCategory.weight.set()
#
#
# @dp.message_handler(state=FinanceCategory.item)
# async def state_item(message: types.Message, state: FSMContext):
#
#     await state.update_data(
#         product_item=int(message.text)
#     )
#
#     data = await state.get_data()
#
#     text = (f"Kategoriya: <b>{data['category_name']}</b>"
#             f"\nSubkategoriya: <b>{data['subcategory_name']}</b>"
#             f"\nMahsulot nomi: <b>{data['product_name']}</b>"
#             f"\nMahsulot vazni/soni: <b>{message.text}</b>")
#     await message.answer(
#         text=f'{text}'
#              f"\n\nNarxni kiriting:"
#              f"{digits}"
#     )
#     await FinanceCategory.price.set()
#
#
# @dp.message_handler(state=FinanceCategory.weight)
# async def state_kg(message: types.Message, state: FSMContext):
#
#     await state.update_data(
#         product_weight=int(message.text)
#     )
#
#     data = await state.get_data()
#
#     text = (f"Kategoriya: <b>{data['category_name']}</b>"
#             f"\nSubkategoriya: <b>{data['subcategory_name']}</b>"
#             f"\nMahsulot nomi: <b>{data['product_name']}</b>"
#             f"Mahsulot vazni/soni: <b>{message.text}</b>")
#
#     await message.answer(
#         text=f'{text}'
#              f'\n\nMahsulot narxini kiriting:'
#              f'{digits}'
#     )
#     await FinanceCategory.price.set()
#
#
# @dp.message_handler(state=FinanceCategory.price)
# async def state_price(message: types.Message, state: FSMContext):
#
#     data = await state.get_data()
#
#     category_name = data['category_name']
#
#     if "'" in category_name:
#         category_name = category_name.replace("'", "`")
#
#     product_name = data['product_name']
#     price = int(message.text)
#     user_id = int(message.from_user.id)
#
#     if 'product_weight' in data.keys():
#         product_weight = data['product_weight']
#
#         await db.add_out(
#             user_id=user_id,
#             category_name=category_name,
#             productname=product_name,
#             price=price,
#             item=product_weight,
#             summary=product_weight * price,
#             weight_or_item='kg'
#         )
#
#     if 'product_item' in data.keys():
#
#         product_item = int(data['product_item'])
#
#         await db.add_out(
#             user_id=user_id,
#             category_name=category_name,
#             productname=product_name,
#             price=price / product_item,
#             item=product_item,
#             summary=price,
#             weight_or_item='dona'
#         )
#
#     await message.answer(
#         text='Mahsulot bazaga qo\'shildi!',
#         reply_markup=await categories_keyboard(user_id=user_id)
#     )
#     await state.finish()
#
#
# @dp.callback_query_handler(text_contains='additem', state='*')
# async def additem(call: types.CallbackQuery):
#
#     product_id = call.data.split('_')[-1]
#
#     product = await db.get_product(product_id=product_id)
