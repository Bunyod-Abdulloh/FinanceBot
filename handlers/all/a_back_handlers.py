from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboards.inline.out_in_keys import main_menu
from loader import dp


@dp.message_handler(text='⬅️ Ortga', state='*')
async def incoming_(message: types.Message, state: FSMContext):

    await message.answer(
        text="<b>Bosh sahifa</b>",
        reply_markup=await main_menu()
    )
    await state.finish()
