import datetime

from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboards.default.start_keyboard import menu
from keyboards.inline.menu_keyboards import summary_or_item_keyboard, categories_keyboard
from loader import dp, db
from states.user_states import FinanceSubcategory


@dp.message_handler(text='Bosh menyu', state='*')
async def main_menu(message: types.Message, state: FSMContext):
    await message.answer(text='Bosh menyu',
                         reply_markup=await categories_keyboard())
    await state.finish()


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
             f'\nMahsulot nomi: <b>{message.text}</b>'
             f'\n\nMahsulot og\'irligi yoki summani kiriting:',
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

    if call.data == 'item':
        await call.message.answer(
            text=f'Category: <b>{category}</b>'
                 f'\nSubcategory: <b>{subcategory}</b>'
                 f'\nMahsulot nomi: <b>{product_name}</b>'
                 f'\n\nMahsulot vaznini kiriting:'
        )
        await FinanceSubcategory.item.set()

    elif call.data == 'summary':
        await call.message.answer(
            text=f'Category: <b>{category}</b>'
                 f'\nSubcategory: <b>{subcategory}</b>'
                 f'\nMahsulot nomi: <b>{product_name}</b>'
                 f'\n\nMahsulot summasini kiriting:'
        )
        await FinanceSubcategory.summary.set()


@dp.message_handler(state=FinanceSubcategory.item)
async def item_subcategory(message: types.Message, state: FSMContext):
    await state.update_data(
        product_item=message.text
    )

    data = await state.get_data()
    category = data['category_name']
    subcategory = data['date']
    product_name = data['product_name']
    product_item = message.text

    await message.answer(
        text=f'Category: <b>{category}</b>'
             f'\nSubcategory: <b>{subcategory}</b>'
             f'\nMahsulot nomi: <b>{product_name}</b>'
             f'\nMahsulot vazni: <b>{product_item} kg</b>'
             f'\n\nMahsulot narxini kiriting:'
    )
    await FinanceSubcategory.price.set()


@dp.message_handler(state=FinanceSubcategory.summary)
async def summary_subcategory(message: types.Message, state: FSMContext):
    data = await state.get_data()

    category_name = data['category_name']
    date = data['date']
    product_name = data['product_name']
    price = int(message.text)

    await db.add_date(
        category_name=category_name,
        date=date,
        productname=product_name,
        price=price,
        item=1,
        summary=price * 1
    )
    await message.answer(text='Mahsulot bazaga qo\'shildi!',
                         reply_markup=await categories_keyboard())
    await state.finish()


@dp.message_handler(state=FinanceSubcategory.price)
async def price_subcategory(message: types.Message, state: FSMContext):

    data = await state.get_data()

    category_name = data['category_name']
    date = data['date']
    product_name = data['product_name']
    product_item = int(data['product_item'])
    price = int(message.text)

    await db.add_date(
        category_name=category_name,
        productname=product_name,
        price=price,
        item=product_item,
        summary=price * product_item,
        date=date
    )

    await message.answer(text='Mahsulot bazaga qo\'shildi!',
                         reply_markup=await categories_keyboard())
    await state.finish()
