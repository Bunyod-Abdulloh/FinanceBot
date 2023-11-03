from aiogram import types

from keyboards.inline.incoming_keyboards import incoming_main_menu
from keyboards.inline.outgoing_keyboards import categories_keyboard
from loader import db


async def replace_point_bottom_line(message):
    if "'" in message:
        incoming = message.replace("'", "`")

    elif "_" in message:
        incoming = message.replace("_", "")

    else:
        incoming = message

    return incoming


async def replace_float(message):
    if "." in message:
        incoming = message.replace(".", "")

    elif "," in message:
        incoming = message.replace(",", "")

    else:
        incoming = message

    return int(incoming)


#  CHECK SUMMARY OUTGOING
async def all_summary_main_out(user_id: int, callback: types.CallbackQuery):
    all_summ = await db.get_sum_all_out(
        user_id=user_id
    )
    if all_summ is None:
        all_summ = 0

    await callback.message.edit_text(
        text=f"<b>📤 Chiqim</b>"
             f"\n\n📤 Chiqim bo'limi uchun jami harajat: <b>{all_summ} so'm</b>",
        reply_markup=await categories_keyboard(user_id=user_id)
    )


# CHECK SUMMARY INCOMING
async def check_summary_main_inc(user_id: int, callback: types.CallbackQuery, no_edit=False):
    all_summary = await db.summary_all_inc(
        user_id=user_id
    )

    if all_summary is None:
        all_summary = 0
    if no_edit:
        await callback.message.answer(
            text=f"<b>📥 Kirim bo'limi</b>"
                 f"\n\n📥 Kirim bo'limi uchun jami: <b>{all_summary}</b> so'm",
            reply_markup=await incoming_main_menu(
                user_id=user_id
            )
        )
    else:
        await callback.message.edit_text(
            text=f"<b>📥 Kirim bo'limi</b>"
                 f"\n\n📥 Kirim bo'limi uchun jami: <b>{all_summary}</b> so'm",
            reply_markup=await incoming_main_menu(
                user_id=user_id
            )
        )


warning_text_uz_latin = ("Bot ishlashida muammo bo'lmasligi uchun kiritilayotgan matnda _, !, ? kabi belgilardan "
                         "foydalanmasligingizni hamda 64 ta belgidan ko'p belgi kiritmaslingizni iltimos qilamiz!")

warning_text_uz_kirill = ("Бот ишлашида муаммо бўлмаслиги учун киритилаётган матнда _, !, ? каби белгилардан"
                          "фойдаланмаслигингизни ҳамда 64 та белгидан кўп белги киритмаслигингизни илтимос қиламиз!")

# warning_text_ru = ("Bot ishlashida muammo bo'lmasligi uchun kiritilayotgan matnda _, !, ? kabi belgilardan "
#                          "foydalanmasligingizni hamda 64 ta belgidan ko'p belgi kiritmaslingizni iltimos qilamiz!")

warning_number_uz_latin = "\n(faqat raqam kiritilishi lozim!):"

warning_number_uz_kirill = "\n(faqat raqam kiritilishi lozim!):"

warning_number_ru = "\n(faqat raqam kiritilishi lozim!):"
