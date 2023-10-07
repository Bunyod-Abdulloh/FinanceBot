from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboards.inline.menu_keyboards import summary_or_item_keyboard
from loader import dp, db
from states.user_states import FinanceSubcategory


@dp.callback_query_handler(text_contains='addsubcategory')
async def add_subcategory(call: types.CallbackQuery, state: FSMContext):
    category = call.data.split('_')[-1]
    await state.update_data(
        category_name=category
    )
    await call.message.answer(
        text='Sanani kiriting:\n\n<b>2023-10-03</b>'
    )
    await FinanceSubcategory.add_date.set()


@dp.message_handler(state=FinanceSubcategory.add_date)
async def update_subcategory(message: types.Message, state: FSMContext):
    await state.update_data(
        date=message.text
    )
    await message.answer(
        text='Mahsulot yoki harajat nomini kiriting:'
    )
    await FinanceSubcategory.add_product.set()


@dp.message_handler(state=FinanceSubcategory.add_product)
async def subcategory_product(message: types.Message, state: FSMContext):
    await state.update_data(
        product_name=message.text
    )
    await message.answer(
        text='Mahsulot soni/og\'irligi yoki summani kiriting:',
        reply_markup=summary_or_item_keyboard()
    )
    await FinanceSubcategory.summary_or_item.set()


@dp.callback_query_handler(state=FinanceSubcategory.summary_or_item)
async def summary_or_item_subcategory(call: types.CallbackQuery):
    await call.message.delete()

    if call.data == 'item':
        await call.message.answer(
            text='Mahsulot soni/og\'irligini kiriting:'
        )
        await FinanceSubcategory.item.set()
    elif call.data == 'summary':
        await call.message.answer(
            text='Mahsulot summasini kiriting:'
        )
        await FinanceSubcategory.summary.set()


@dp.message_handler(state=FinanceSubcategory.item)
async def item_subcategory(message: types.Message, state: FSMContext):
    await state.update_data(
        product_item=message.text
    )
    await message.answer(
        text='Mahsulot narxini kiriting:'
    )
    await FinanceSubcategory.price.set()


@dp.message_handler(state=FinanceSubcategory.summary)
async def summary_subcategory(message: types.Message, state: FSMContext):
    summary = int(message.text)

    data = await state.get_data()
    print(data)

    # await db.add_date(
    #     category_name=data['category_name'],
    #     productname=data['product_name'],
    #     price=price,
    #     item=1,
    #     summary=price * 1,
    #     date=
    # )


@dp.message_handler(state=FinanceSubcategory.price)
async def price_subcategory(message: types.Message, state: FSMContext):

    price = int(message.text)

    data = await state.get_data()

    category_name = data['category_name']
    date = data['date']
    product_name = data['product_name']

