from aiogram import types
from aiogram.dispatcher import FSMContext

from aiogram.dispatcher.filters.builtin import CommandStart

from keyboards.inline.out_in_keys import main_menu
from loader import dp, db

category_name = ["Kommunal to`lovlar", "Internet", "Telefon"]
subcategory_name = ["Issiq suv", "Sovuq suv", "Elektr energiya", "Gaz", "Uy", "Mening raqamim"]


@dp.message_handler(CommandStart(), state='*')
async def bot_start(message: types.Message, state: FSMContext):

    await message.answer(
        text="IqtisodchiRobotga xush kelibsiz!",
        reply_markup=await main_menu()
    )
    await state.finish()

    user_id = int(message.from_user.id)
    summary = 0
    
    for n in range(100):
        summary += 1
        await db.add_outgoing(
            category_name=category_name[0],
            subcategory_name=subcategory_name[0],
            user_id=user_id,
            summary=summary
        )
        await db.add_outgoing(
            category_name=category_name[0],
            subcategory_name=subcategory_name[1],
            user_id=user_id,
            summary=summary
        )
        await db.add_outgoing(
            category_name=category_name[0],
            subcategory_name=subcategory_name[2],
            user_id=user_id,
            summary=summary
        )
        await db.add_outgoing(
            category_name=category_name[0],
            subcategory_name=subcategory_name[3],
            user_id=user_id,
            summary=summary
        )
        await db.add_outgoing(
            category_name=category_name[1],
            subcategory_name=subcategory_name[4],
            user_id=user_id,
            summary=summary
        )
        await db.add_outgoing(
            category_name=category_name[2],
            subcategory_name=subcategory_name[5],
            user_id=user_id,
            summary=summary
        )
    # await db.add_outgoing(
    #             category_name="Telefon",
    #             subcategory_name='O\'zim',
    #             user_id=user_id, summary=summary
    #         )


@dp.callback_query_handler(text='back_main_menu', state='*')
async def back_main_menu(call: types.CallbackQuery, state: FSMContext):
    await call.message.edit_text(
        text='Bosh menu',
        reply_markup=await main_menu()
    )
    await state.finish()
