from aiogram import types

from keyboards.inline.menu_keyboards import categories_keyboard
from loader import dp, db


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
