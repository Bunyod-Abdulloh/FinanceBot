import datetime

from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboards.default.start_keyboard import menu
from keyboards.inline.menu_keyboards import summary_or_item_keyboard, categories_keyboard
from loader import dp, db
from states.user_states import FinanceSubcategory


@dp.callback_query_handler(text_contains='addsubcategory')
async def add_subcategory(call: types.CallbackQuery, state: FSMContext):
    category_name = call.data.split('_')[-1]
    await state.update_data(
        category_name=category_name
    )
    await call.message.delete()

    await call.message.answer(
        text=f'Category: <b>{category_name}</b>'
             f'\n\nSanani kiriting:\n<b>2023-10-03</b>',
        reply_markup=menu
    )
    await FinanceSubcategory.add_date.set()


@dp.message_handler(state=FinanceSubcategory.add_date)
async def update_subcategory(message: types.Message, state: FSMContext):

    date_state = message.text
    date_split = date_state.split('-')
    date = datetime.date(year=int(date_split[0]),
                         month=int(date_split[1]),
                         day=int(date_split[2]))
    await state.update_data(
        date=date
    )
    data = await state.get_data()

    await message.answer(
        text=f'Category: <b>{data["category_name"]}</b>'
             f'\nSubcategory: <b>{message.text}</b>'
             f'\n\nMahsulot yoki harajat nomini kiriting:'
    )
    await FinanceSubcategory.add_product.set()


@dp.message_handler(state=FinanceSubcategory.add_product)
async def subcategory_product(message: types.Message, state: FSMContext):
    await state.update_data(
        product_name=message.text
    )
    data = await state.get_data()

    await message.answer(
        text=f'Category: <b>{data["category_name"]}</b>'
             f'\nSubcategory: <b>{data["date"]}</b>'
             f'\nProduct_name: <b>{message.text}</b>'
             f'\n\nMahsulot soni yoki vaznini kiriting:'
             f'\n(faqat raqam kiritilishi lozim!',
        reply_markup=summary_or_item_keyboard()
    )
    await FinanceSubcategory.summary_or_item.set()


@dp.callback_query_handler(state=FinanceSubcategory.summary_or_item)
async def summary_or_item_subcategory(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()

    data = await state.get_data()

    category = data['category_name']
    subcategory = data['date']
    product_name = data['product_name']

    text = (f'Category: <b>{category}</b>'
            f'\nSubcategory: <b>{subcategory}</b>'
            f'\nProduct_name: <b>{product_name}</b>')

    if call.data == 'item':
        await call.message.answer(
            text=f'{text}'
                 f'\n\nMahsulot sonini kiriting:'
                 f'\n(faqat raqam kiritilishi lozim!)'
        )
        await FinanceSubcategory.item.set()

    elif call.data == 'item_kg':
        await call.message.answer(
            text=f'{text}'
                 f'\n\nMahsulot vaznini kiriting:'
                 f'\n(faqat raqam kiritilishi lozim!)'
        )
        await FinanceSubcategory.weight.set()


@dp.message_handler(state=FinanceSubcategory.item)
async def item_subcategory(message: types.Message, state: FSMContext):
    product_item = int(message.text)

    await state.update_data(
        product_item=product_item
    )

    data = await state.get_data()
    category = data['category_name']
    subcategory = data['date']
    product_name = data['product_name']

    text = (f'Category: <b>{category}</b>'
            f'\nSubcategory: <b>{subcategory}</b>'
            f'\nProduct_name: <b>{product_name}</b>'
            f'\nProduct_quantity: <b>{product_item}</b>')

    await message.answer(
        text=f'{text}'
             f'\n\nNarxni kiriting:'
             f'\n(faqat raqam kiritilishi lozim!'
    )
    await FinanceSubcategory.price.set()


@dp.message_handler(state=FinanceSubcategory.weight)
async def state_weight_subcategory(message: types.Message, state: FSMContext):
    print(type(message.text))

    product_weight = int(message.text)

    await state.update_data(
        product_weight=product_weight
    )

    data = await state.get_data()

    text = (f'Category: <b>{data["category_name"]}</b>\n'
            f'Product_name: <b>{data["product_name"]}</b>\n'
            f'Product_weight: <b>{message.text}</b>')

    await message.answer(
        text=f'{text}'
             f'\n\nMahsulot narxini kiriting:'
             f'\n(faqat raqam kiritilishi lozim!)'
    )
    await FinanceSubcategory.price.set()


@dp.message_handler(state=FinanceSubcategory.price)
async def price_subcategory(message: types.Message, state: FSMContext):

    data = await state.get_data()

    category_name = data['category_name']
    date = data['date']
    product_name = data['product_name']
    price = int(message.text)

    if 'product_weight' in data.keys():
        product_weight = data['product_weight']

        await db.add_date(
            category_name=category_name,
            date=date,
            productname=product_name,
            price=price,
            item=product_weight,
            summary=product_weight * price,
            weight_or_item='kg'
        )

    if 'product_item' in data.keys():
        product_item = int(data['product_item'])

        await db.add_date(
            category_name=category_name,
            date=date,
            productname=product_name,
            price=price / product_item,
            item=product_item,
            summary=price,
            weight_or_item='dona'
        )

    await message.answer(text='Mahsulot bazaga qo\'shildi!',
                         reply_markup=await categories_keyboard())
    await state.finish()
