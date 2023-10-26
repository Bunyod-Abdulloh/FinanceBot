from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboards.inline.outgoing_keyboards import categories_keyboard
from loader import dp, db
from states.user_states import FinanceEdit


@dp.callback_query_handler(text_contains='editproduct', state='*')
async def state_edit_product(call: types.CallbackQuery, state: FSMContext):

    await call.message.delete()

    old_product_id = int(call.data.split('_')[-1])

    await state.update_data(
        old_product_id=old_product_id
    )

    await call.message.answer(
        text='Mahsulot uchun yangi nom kiriting:'
    )

    await FinanceEdit.product.set()


@dp.message_handler(state=FinanceEdit.product)
async def state_edit_product_(message: types.Message, state: FSMContext):
    data = await state.get_data()

    await db.update_product_name(
        old_product_id=data['old_product_id'],
        new_product=message.text
    )

    await message.answer(
        text='Mahsulot nomi o\'zgartirildi!',
        reply_markup=await categories_keyboard()
    )

    await state.finish()
