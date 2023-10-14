from aiogram import types
from aiogram.dispatcher import FSMContext

from aiogram.dispatcher.filters.builtin import CommandStart

from keyboards.inline.out_keyboards import main_menu

from loader import dp, db

category_name = ["Kommunal to'lovlar", "Internet", "Telefon"]
subcategory_name = ["Elektr energiya", "Ichimlik suv", "Issiq suv", "Chiqindi", "Uy", "O'zim"]

for n in category_name:
    if "'" in category_name:
    category_name = category_name.replace("'", "`")

@dp.message_handler(CommandStart(), state='*')
async def bot_start(message: types.Message, state: FSMContext):

    await message.answer(
        text="FinanceBotga xush kelibsiz!",
        reply_markup=await main_menu()
    )
    await state.finish()

    user_id = int(message.from_user.id)

    await db.first_add_out(
        category_name=,
        subcategory_name='Elektr energiya',
        user_id=user_id
    )
    await db.first_add_out(
            category_name="Kommunal to'lovlar",
            subcategory_name='Ichimlik suvi',
            user_id=user_id
        )
    await db.first_add_out(
            category_name="Kommunal to'lovlar",
            subcategory_name='Gaz',
            user_id=user_id
        )
    await db.first_add_out(
            category_name="Kommunal to'lovlar",
            subcategory_name='Chiqindi',
            user_id=user_id
        )
    await db.first_add_out(
                category_name="Kommunal to'lovlar",
                subcategory_name='Issiq suv va issiqlik ta\'minoti',
                user_id=user_id
            )
    await db.first_add_out(
                category_name="Internet",
                subcategory_name='Uy',
                user_id=user_id
            )
    await db.first_add_out(
                category_name="Telefon",
                subcategory_name='O\'zim',
                user_id=user_id
            )


@dp.callback_query_handler(text='back_main_menu', state='*')
async def back_main_menu(call: types.CallbackQuery, state: FSMContext):
    await call.message.edit_text(
        text='Bosh menu',
        reply_markup=await main_menu()
    )
    await state.finish()
