import asyncpg
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandStart

from keyboards.inline.menu_keyboards import main_menu

from loader import dp
from data.config import ADMINS


@dp.message_handler(CommandStart(), state='*')
async def bot_start(message: types.Message):

    if str(message.from_user.id) in ADMINS:
        # all_categories = await db.get_categories()
        # current_page = 1
        #
        # if len(all_categories) % PAGE_COUNT == 0:
        #     all_pages = len(all_categories) // PAGE_COUNT
        # else:
        #     all_pages = len(all_categories) // PAGE_COUNT + 1
        # # 200 // 25
        # key = buttons_generator(database=all_categories[:PAGE_COUNT],
        #                         current_page=current_page,
        #                         all_pages=all_pages)
        await message.answer(
            text="FinanceBotga xush kelibsiz!",
            reply_markup=main_menu()
        )
