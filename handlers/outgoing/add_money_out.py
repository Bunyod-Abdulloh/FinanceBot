import logging

from aiogram import types
from aiogram.dispatcher import FSMContext

from handlers.all.all_functions import replace_float
from keyboards.inline.outgoing_keyboards import items_keyboard, subcategories_keyboard
from loader import dp, db
from states.user_states import MoneyOut


# ======================ADD_MONEY======================
@dp.callback_query_handler(text_contains="addmoney", state="*")
async def ph_addmoney(call: types.CallbackQuery, state: FSMContext):

    product_id = call.data.split("_")[1]

    product = await db.get_product_out(product_id=product_id)

    await state.update_data(
        category_name=product[0],
        subcategory_name=product[1]
    )

    await call.message.edit_text(
        text=f"Bo'lim: <b>Chiqim</b>"
             f"\nKategoriya: <b>{product[0]}</b>"
             f"\nSubkategoriya: <b>{product[1]}</b>"
             f"\n\nQo'shmoqchi bo'lgan summangizni kiriting:"
    )

    await MoneyOut.add_money.set()


@dp.message_handler(state=MoneyOut.add_money)
async def add_money_out(message: types.Message, state: FSMContext):
    try:
        data = await state.get_data()
        category = data['category_name']
        subcategory = data['subcategory_name']
        user_id = message.from_user.id

        money = await replace_float(message=message.text)

        await db.first_add_out(category_name=category,
                               subcategory_name=subcategory,
                               summary=money,
                               user_id=user_id)

        await message.answer(text="Summa qo'shildi")

        await message.answer(
            text=f"Bo'lim: <b>Chiqim</b>"
                 f"\nKategoriya: <b>{category}</b>"
                 f"\nSubkategoriya: <b>{subcategory}</b>",
            reply_markup=await subcategories_keyboard(
                user_id=user_id,
                category_name=category
            )
        )

        await state.finish()
    except Exception as err:
        await message.answer(text="<b>Xatolik❗️❗️❗️"
                                  "\n\nIltimos, qayta /start buyrug'ini kiriting!</b>")
        logging.error(err)

# ======================REDUCE_AMOUNT======================
# @dp.callback_query_handler(text_contains="reduceamount", state="*")
# async def ph_addmoney(call: types.CallbackQuery, state: FSMContext):
#
#     product_id = call.data.split("_")[1]
#
#     product = await db.get_product_out(product_id=product_id)
#
#     await state.update_data(
#         product_id=product_id,
#         summary=product[2]
#     )
#
#     await call.message.edit_text(
#         text=f"Bo'lim: <b>Chiqim</b>"
#              f"\nKategoriya: <b>{product[0]}</b>"
#              f"\nSubkategoriya: <b>{product[1]}</b>"
#              f"\n\nAyirmoqchi bo'lgan summangizni kiriting:"
#     )
#
#     await MoneyOut.reduce_amount.set()
#
#
# @dp.message_handler(state=MoneyOut.reduce_amount)
# async def add_money_out(message: types.Message, state: FSMContext):
#     try:
#         data = await state.get_data()
#
#         money = await replace_float(message=message.text)
#         user_id = message.from_user.id
#
#         if data['summary'] < money:
#             await message.answer(text="Xatolik❗️❗️❗️")
#
#         else:
#             await db.update_productsum_out(summary=data['summary'] - money,
#                                            product_id=int(data['product_id']),
#                                            user_id=user_id)
#
#             await message.answer(text="Summa ayirildi!",
#                                  reply_markup=await categories_keyboard(user_id=user_id))
#             await state.finish()
#     except Exception:
#         await message.answer(text="<b>Xatolik❗️❗️❗️"
#                                   "\n\nIltimos, qayta /start buyrug'ini kiriting!</b>")

