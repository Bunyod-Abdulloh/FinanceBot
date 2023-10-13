from aiogram import types

from aiogram.dispatcher.filters.builtin import CommandStart

from keyboards.inline.out_keyboards import main_menu

from loader import dp


@dp.message_handler(CommandStart(), state='*')
async def bot_start(message: types.Message):

    await message.answer(
        text="FinanceBotga xush kelibsiz!",
        reply_markup=await main_menu()
    )
