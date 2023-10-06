import asyncpg
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandStart
from keyboards.inline.menu_keyboards import categories_keyboard

from loader import dp
from data.config import ADMINS


@dp.message_handler(CommandStart(), state='*')
async def bot_start(message: types.Message):

    if str(message.from_user.id) in ADMINS:
        await message.answer(
            text='FinanceBotga xush kelibsiz!',
            reply_markup=await categories_keyboard())
