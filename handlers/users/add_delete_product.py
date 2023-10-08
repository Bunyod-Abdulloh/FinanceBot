import datetime

from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboards.inline.menu_keyboards import categories_keyboard
from loader import dp, db
from states.user_states import FinanceSubcategory


@dp.callback_query_handler(text_contains='deleteproduct', state='*')
async def editProduct(call: types.CallbackQuery):

    product_id = int(call.data.split('_')[-1])
    await db.delete_products(
        product_id=product_id
    )

    await call.message.answer(
        text='Mahsulot bazadan o\'chirildi!',
        reply_markup=await categories_keyboard()
    )
    await call.message.delete()


@dp.callback_query_handler(text_contains='addproduct', state='*')
async def addproduct(call: types.CallbackQuery, state: FSMContext):

    category = call.data.split('_')[1]

    date_ = call.data.split('_')[-1]
    date_state = date_
    date_split = date_state.split('-')
    date = datetime.date(year=int(date_split[0]),
                         month=int(date_split[1]),
                         day=int(date_split[2]))

    await state.update_data(
        category_name=category,
        date=date
    )

    await call.message.delete()

    await call.message.answer(
        text='Mahsulot yoki harajat nomini kiriting:'
    )
    await FinanceSubcategory.add_product.set()
