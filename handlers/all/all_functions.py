from aiogram import types

from keyboards.inline.outgoing_keyboards import categories_keyboard
from loader import db


#  CHECK SUMMARY OUTGOING
async def all_summary_main_out(
        user_id: int,
        callback: types.CallbackQuery,
        section_name: str,
        total: str,
        currency: str
):
    all_summ = await db.get_summary_out(
        all_outgoing=True,
        user_id=user_id
    )
    if all_summ is None:
        all_summ = 0

    await callback.message.edit_text(
        text=f"<b>{section_name}</b>"
             f"\n\n{total}: <b>{all_summ} {currency}</b>",
        reply_markup=await categories_keyboard(user_id=user_id)
    )

warning_text_uz_latin = ("Bot ishlashida muammo bo'lmasligi uchun faqat harflar kiritilishi hamda ularning "
                         "uzunligi 64 tadan oshmasligi lozim!")

warning_text_uz_kirill = ("Бот ишлашида муаммо бўлмаслиги учун киритилаётган матнда _, !, ? каби белгилардан"
                          "фойдаланмаслигингизни ҳамда 64 та белгидан кўп белги киритмаслигингизни илтимос қиламиз!")

# warning_text_ru = ("Bot ishlashida muammo bo'lmasligi uchun kiritilayotgan matnda _, !, ? kabi belgilardan "
#                          "foydalanmasligingizni hamda 64 ta belgidan ko'p belgi kiritmaslingizni iltimos qilamiz!")

warning_number_uz_latin = "\n\n(faqat raqam kiritilishi lozim!\nMasalan: 15000)"

warning_number_uz_kirill = "\n(faqat raqam kiritilishi lozim!):"

warning_number_ru = "\n(faqat raqam kiritilishi lozim!):"
