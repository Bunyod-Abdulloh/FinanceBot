import asyncio
import logging
import os

from aiogram import types
from aiogram.dispatcher import FSMContext
from openpyxl import Workbook

from keyboards.inline.out_keyboards import back_download
from loader import bot, db, dp


@dp.callback_query_handler(text="downloadall", state="*")
async def dc_category_one(call: types.CallbackQuery, state: FSMContext):
    try:
        await call.message.delete()

        user_id = call.from_user.id
        category = await db.get_categories_out(user_id=user_id)
        all_summary = await db.get_sum_all_out(user_id=user_id)

        wb = Workbook()

        ws = wb.active

        ws.append(["Bo'lim nomi", "Summa (so'm)"])

        for data in category:
            summary = await db.get_sum_category(user_id=user_id, category_name=data[0])

            ws.append([data[0], summary])

        ws.append(["Jami:", f"{all_summary}"])

        wb.save("Misol.xlsx")

        await bot.send_document(chat_id=user_id,
                                document=types.InputFile(path_or_bytesio="Misol.xlsx"),
                                reply_markup=back_download)

        os.remove("Misol.xlsx")
    except Exception as err:
        logging.error(err)
