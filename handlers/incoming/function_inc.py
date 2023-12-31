import asyncio

from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboards.inline.history_ikeys import PAGE_COUNT, buttons_generator
from keyboards.inline.incoming_keyboards import incoming_main_menu
from loader import db


# CHECK SUMMARY INCOMING
async def check_summary_main_inc(user_id: int, callback: types.CallbackQuery, section_name: str, total: str,
                                 currency: str, no_edit=False):
    all_summary = await db.summary_all_inc(
        user_id=user_id
    )
    if all_summary is None:
        all_summary = 0
    if no_edit:
        await callback.message.answer(
            text=f"<b>{section_name}</b>"
                 f"\n\n{total} <b>{all_summary}</b> {currency}",
            reply_markup=await incoming_main_menu(
                user_id=user_id
            )
        )
    else:
        await callback.message.edit_text(
            text=f"<b>{section_name}</b>"
                 f"\n\n{total}: <b>{all_summary}</b> {currency}",
            reply_markup=await incoming_main_menu(
                user_id=user_id
            )
        )


# BUTTONS GENERATOR

async def first_all_history_button_inc(
        current_page: int,
        database: list,
        back_button: str,
        call: types.CallbackQuery,
        language: str,
        state: FSMContext,
        currency: str,
        all_summary: int
):
    if len(database) % PAGE_COUNT == 0:
        all_pages = len(database) // PAGE_COUNT
    else:
        all_pages = len(database) // PAGE_COUNT + 1

    key = buttons_generator(current_page=current_page, all_pages=all_pages,
                            subcategory=back_button, incoming_main=True)
    for data in database[:PAGE_COUNT]:
        summary = await db.summary_category_inc(
            user_id=call.from_user.id,
            incoming_name=data[0]
        )
        await db.update_inc_history(
            user_id=call.from_user.id,
            history=f"{data[0]} | {summary} {currency}\n"
        )

    history = await db.get_user_inc(user_id=call.from_user.id,
                                    history=True)

    if language == "uz_latin":
        await call.message.answer(
            text=f"<b>📥 Kirim > 📜 Kirimlar tarixi</b>"
                 f"\n\n{history[0]}\n📥 Kirim bo'limi uchun jami: {all_summary} {currency}",
            reply_markup=key
        )
    if language == "uz_cyrillic":
        pass
    if language == "ru":
        pass

    await db.clear_history_inc(user_id=call.from_user.id)

    await state.update_data(
        current_page=current_page,
        all_pages=all_pages
    )


async def second_all_history_button_inc(
        call: types.CallbackQuery,
        current_page: int,
        all_pages: int,
        database: list,
        language: str,
        back_button: str,
        currency: str,
        all_summary: int,
        state: FSMContext
):
    if call.data == "prev":
        if current_page == 1:
            current_page = all_pages
        else:
            current_page -= 1
    if call.data == 'next':
        if current_page == all_pages:
            current_page = 1
        else:
            current_page += 1

    all_messages = database[(current_page - 1) * PAGE_COUNT: current_page * PAGE_COUNT]

    key = buttons_generator(current_page=current_page, all_pages=all_pages,
                            subcategory=back_button, incoming_main=True)

    for data in all_messages:
        summary = await db.summary_category_inc(
            user_id=call.from_user.id,
            incoming_name=data[0]
        )
        await db.update_inc_history(
            user_id=call.from_user.id,
            history=f"{data[0]} | {summary} {currency}\n"
        )

    history = await db.get_user_inc(user_id=call.from_user.id,
                                    history=True)

    if language == 'uz_latin':
        await call.message.answer(
            text=f"<b>📥 Kirim > 📜 Kirimlar tarixi</b>"
                 f"\n\n{history[0]}\n📥 Kirim bo'limi uchun jami: {all_summary} {currency}",
            reply_markup=key
        )

    if language == 'uz_cyrillic':
        pass

    if language == 'ru':
        pass

    await db.clear_history_inc(user_id=call.from_user.id)

    await state.update_data(
        current_page=current_page,
        all_pages=all_pages
    )


async def first_category_history_button_inc(
        current_page: int,
        database: list,
        language: str,
        currency: str,
        call: types.CallbackQuery,
        section_name: str,
        section_summary: int,
        state: FSMContext
):
    if len(database) % PAGE_COUNT == 0:
        all_pages = len(database) // PAGE_COUNT
    else:
        all_pages = len(database) // PAGE_COUNT + 1

    key = buttons_generator(current_page=current_page, all_pages=all_pages,
                            subcategory=section_name, incoming_category=True)
    for data in database[:PAGE_COUNT]:
        await db.update_inc_history(
            user_id=call.from_user.id,
            history=f"{data[2]} | {data[0]} | {data[1]} {currency}\n"
        )

    history = await db.get_user_inc(user_id=call.from_user.id,
                                    history=True)

    if language == 'uz_latin':
        await call.message.answer(
            text=f"<b>📥 Kirim > 📜 Kirimlar tarixi > {section_name}</b>"
                 f"\n\n{history[0]}\n{section_name} uchun jami: {section_summary} {currency}",
            reply_markup=key
        )
    if language == 'uz_cyrillic':
        pass
    if language == 'ru':
        pass

    await db.clear_history_inc(user_id=call.from_user.id)

    await state.update_data(
        current_page=current_page,
        all_pages=all_pages
    )


async def second_category_history_button_inc(
        call: types.CallbackQuery,
        current_page: int,
        all_pages: int,
        database: list,
        section_name: str,
        section_summary: str,
        currency: str,
        language: str,
        state: FSMContext
):
    if call.data == "prev":
        if current_page == 1:
            current_page = all_pages
        else:
            current_page -= 1
    if call.data == 'next':
        if current_page == all_pages:
            current_page = 1
        else:
            current_page += 1

    all_messages = database[(current_page - 1) * PAGE_COUNT: current_page * PAGE_COUNT]

    key = buttons_generator(current_page=current_page, all_pages=all_pages,
                            subcategory=section_name, incoming_category=True)

    for data in all_messages:
        await db.update_inc_history(
            user_id=call.from_user.id,
            history=f"{data[2]} | {data[0]} | {data[1]} {currency}\n"
        )

    history = await db.get_user_inc(user_id=call.from_user.id,
                                    history=True)

    if language == "uz_latin":
        await call.message.answer(
            text=f"<b>📥 Kirim > 📜 Kirimlar tarixi > {section_name}</b>"
                 f"\n\n{history[0]}\n{section_name} uchun jami: {section_summary} {currency}",
            reply_markup=key
        )
    if language == "uz_cyrillic":
        pass
    if language == "ru":
        pass

    await db.clear_history_inc(user_id=call.from_user.id)

    await state.update_data(
        current_page=current_page, all_pages=all_pages
    )
