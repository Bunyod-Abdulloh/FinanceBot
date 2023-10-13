from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboards.inline.out_keyboards import summary_or_item_keyboard, categories_keyboard
from loader import dp, db
from states.user_states import FinanceCategory


@dp.callback_query_handler(text='add_category', state='*')
async def add_category_call(call: types.CallbackQuery):

    await call.message.edit_text(
        text='Kategoriya nomini kiriting:')
    await FinanceCategory.add_category.set()


@dp.message_handler(state=FinanceCategory.add_category)
async def add_category(message: types.Message, state: FSMContext):
    await state.update_data(
        category_name=message.text
    )

    await message.answer(
        text=f'Category: <b>{message.text}</b>'
             f'\n\nMahsulot yoki harajat nomini kiriting:'
    )
    await FinanceCategory.add_product.set()


@dp.message_handler(state=FinanceCategory.add_product)
async def add_product(message: types.Message, state: FSMContext):
    await state.update_data(
        product_name=message.text
    )

    data = await state.get_data()

    await message.answer(
        text=f'Category: <b>{data["category_name"]}</b>\n'
             f'Product_name: <b>{message.text}</b>'
             f'\n\nMahsulot soni yoki vaznini kiriting:'
             f'\n(faqat raqam kiritilishi lozim!)',
        reply_markup=summary_or_item_keyboard()
    )
    await FinanceCategory.summary_or_item.set()


@dp.callback_query_handler(state=FinanceCategory.summary_or_item)
async def summary_or_item(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()

    data = await state.get_data()
    text = (f'Category: <b>{data["category_name"]}</b>\n'
            f'Product_name: <b>{data["product_name"]}</b>')

    if call.data == 'item':
        await call.message.answer(
            text=f'{text}'
                 f'\n\nMahsulot sonini kiriting:'
                 f'\n(faqat raqam kiritilishi lozim!)'
        )
        await FinanceCategory.item.set()

    elif call.data == 'item_kg':
        await call.message.answer(
            text=f'{text}'
                 f'\n\nMahsulot vaznini kiriting:'
                 f'\n(faqat raqam kiritilishi lozim!)'
        )
        await FinanceCategory.weight.set()


@dp.message_handler(state=FinanceCategory.item)
async def state_item(message: types.Message, state: FSMContext):

    await state.update_data(
        product_item=int(message.text)
    )

    data = await state.get_data()

    text = (f'Category: <b>{data["category_name"]}</b>\n'
            f'Product_name: <b>{data["product_name"]}</b>\n'
            f'Product_quantity: <b>{message.text}</b>')
    await message.answer(
        text=f'{text}'
             f'\n\nNarxni kiriting:'
             f'\n(faqat raqam kiritilishi lozim!)'
    )
    await FinanceCategory.price.set()


@dp.message_handler(state=FinanceCategory.weight)
async def state_kg(message: types.Message, state: FSMContext):

    await state.update_data(
        product_weight=int(message.text)
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
    await FinanceCategory.price.set()


@dp.message_handler(state=FinanceCategory.price)
async def state_price(message: types.Message, state: FSMContext):

    data = await state.get_data()

    category_name = data['category_name']

    if "'" in category_name:
        category_name = category_name.replace("'", "`")

    product_name = data['product_name']
    price = int(message.text)

    if 'product_weight' in data.keys():
        product_weight = data['product_weight']

        await db.add_outgoing(
            category_name=category_name,
            productname=product_name,
            price=price,
            item=product_weight,
            summary=product_weight * price,
            weight_or_item='kg'
        )

    if 'product_item' in data.keys():

        product_item = int(data['product_item'])

        await db.add_outgoing(
            category_name=category_name,
            productname=product_name,
            price=price / product_item,
            item=product_item,
            summary=price,
            weight_or_item='dona'
        )

    await message.answer(
        text='Mahsulot bazaga qo\'shildi!',
        reply_markup=await categories_keyboard()
    )
    await state.finish()


@dp.callback_query_handler(text_contains='additem', state='*')
async def additem(call: types.CallbackQuery):

    product_id = call.data.split('_')[-1]

    product = await db.get_product(product_id=product_id)

    print(product)
