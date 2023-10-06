from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboards.inline.menu_keyboards import summary_or_item_keyboard, categories_keyboard
from loader import dp, db
from states.user_states import FinanceUser


@dp.callback_query_handler(text='add_category', state='*')
async def add_category_call(call: types.CallbackQuery):

    await call.message.edit_text(
        text='Kategoriya nomini kiriting:')
    await FinanceUser.add_category.set()


@dp.message_handler(state=FinanceUser.add_category)
async def add_category(message: types.Message, state: FSMContext):
    await state.update_data(
        category_name=message.text
    )

    await message.answer(
        text='Mahsulot yoki harajat nomini kiriting:'
    )
    await FinanceUser.add_product.set()


@dp.message_handler(state=FinanceUser.add_product)
async def add_product(message: types.Message, state: FSMContext):
    await state.update_data(
        product_name=message.text
    )

    await message.answer(
        text='Mahsulot soni/og\'irligi yoki summani kiriting:',
        reply_markup=summary_or_item_keyboard()
    )
    await FinanceUser.summary_or_item.set()


@dp.callback_query_handler(state=FinanceUser.summary_or_item)
async def summary_or_item(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()

    if call.data == 'item':
        await call.message.answer(
            text='Mahsulot soni/og\'irligini kiriting:'
        )
        await FinanceUser.item.set()
    elif call.data == 'summary':
        await call.message.answer(
            text='Mahsulot summasini kiriting:'
        )
        await FinanceUser.summary.set()


@dp.message_handler(state=FinanceUser.item)
async def state_item(message: types.Message, state: FSMContext):

    await state.update_data(
        product_item=message.text
    )

    await message.answer(
        text='Mahsulot narxini kiriting:'
    )
    await FinanceUser.price.set()


@dp.message_handler(state=FinanceUser.summary)
async def state_summary(message: types.Message, state: FSMContext):
    price = int(message.text)

    data = await state.get_data()

    await db.add_all(
        category_name=data['category_name'],
        productname=data['product_name'],
        price=price,
        item=1,
        summary=price * 1
    )

    await message.answer(
        text='Mahsulot bazaga qo\'shildi!',
        reply_markup=await categories_keyboard()
    )
    await state.finish()


@dp.message_handler(state=FinanceUser.price)
async def state_price(message: types.Message, state: FSMContext):

    data = await state.get_data()
    price = int(message.text)
    item = int(data['product_item'])

    await db.add_all(
        category_name=data['category_name'],
        productname=data['product_name'],
        price=price,
        item=item,
        summary=price * item
    )

    await message.answer(
        text='Mahsulot bazaga qo\'shildi!',
        reply_markup=await categories_keyboard()
    )
    await state.finish()


@dp.callback_query_handler(text_contains='addproduct', state='*')
async def addproduct(call: types.CallbackQuery, state: FSMContext):

    category = call.data.split('_')[1]
    date = call.data.split('_')[-1]
    await state.update_data(
        category_name=category,
        date=date
    )
    await call.message.answer(
        text='Mahsulot yoki harajat nomini kiriting:'
    )
    await FinanceUser.add_product.set()


@dp.callback_query_handler(text_contains='additem', state='*')
async def additem(call: types.CallbackQuery):

    product_id = call.data.split('_')[-1]

    product = await db.get_product(product_id=product_id)

    print(product)
