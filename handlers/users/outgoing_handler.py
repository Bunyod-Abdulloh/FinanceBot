from aiogram import types

from keyboards.inline.menu_keyboards import buttons_generator
from loader import dp, db

PAGE_COUNT = 25


@dp.callback_query_handler(text='outgoing', state='*')
async def outgoing_(call: types.CallbackQuery):
    all_categories = await db.get_categories()
    current_page = 1

    if len(all_categories) % PAGE_COUNT == 0:
        all_pages = len(all_categories) // PAGE_COUNT
    else:
        all_pages = len(all_categories) // PAGE_COUNT + 1
    # 200 // 25
    key = buttons_generator(database=all_categories[:PAGE_COUNT],
                            current_page=current_page,
                            all_pages=all_pages)
    await call.message.edit_text(
        text='Chiqimlar bo\'limi',
        reply_markup=key
    )
