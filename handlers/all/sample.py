import logging
import os
from aiogram import Bot, Dispatcher, executor, types
from aiogram.bot.api import TelegramAPIServer
from aiogram.contrib.middlewares.i18n import I18nMiddleware
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
# from call_back_data import cbd
# import config
from pathlib import Path
# import locales
# import faq
from aiogram.utils.callback_data import CallbackData


class Question(StatesGroup):
    question = State()


class Button(StatesGroup):
    back = State()
    menu = State()


user_language = "en"
cfg = config.get_config()
image_path: str = cfg.IMAGE_PATH
#
# BASE_DIR=Path( __file__ ).parent
# LOCALES_DIR=BASE_DIR.joinpath( cfg.BOT_LOCALES_DIR )
# Configure logging
logging.basicConfig(level=logging.INFO)
local_server = TelegramAPIServer.from_base(base=cfg.LOCAL_BOT_SERVER_HOST)
# Initialize bot and dispatcher
bot = Bot(
    token=cfg.BOT_TOKEN,
    parse_mode="HTML",
)
dp = Dispatcher(
    bot,
    storage=MemoryStorage(),
)
user_data = {}


@dp.message_handler(commands=["start"])
async def send_welcome(message: types.Message, state: FSMContext):
    await state.set_state(Button.menu)
    user_language = message.from_user.locale.language
    saved_user_language = user_data.get(message.from_user.id, user_language)
    await message.reply(
        text=locales.get_locales("start_command", saved_user_language),
        parse_mode="HTML",
    )
    saved_user_language = user_data.get(message.from_user.id, user_language)
    kb = [
        [types.KeyboardButton(text=locales.get_locales("faq", saved_user_language))],
        [types.KeyboardButton(text=locales.get_locales("buy", saved_user_language))],
        [types.KeyboardButton(text=locales.get_locales("lang", saved_user_language))],
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb)
    await message.answer(
        locales.get_locales("menu", saved_user_language), reply_markup=keyboard
    )


@dp.message_handler(
    commands="lang",
)
async def cmd_lang(message: types.Message):
    saved_user_language = user_data.get(message.from_user.id, user_language)
    inline_keyboard = types.InlineKeyboardMarkup(row_width=3)
    inline_keyboard.add(
        types.InlineKeyboardButton(text="English", callback_data=cbd.new(action="en")),
        types.InlineKeyboardButton(text="Uzbek", callback_data=cbd.new(action="uz")),
        types.InlineKeyboardButton(text="Russian", callback_data=cbd.new(action="ru")),
    )
    await message.answer(
        text=locales.get_locales("lang_command", saved_user_language),
        reply_markup=inline_keyboard,
    )


@dp.callback_query_handler(cbd.filter(action=["en", "uz", "ru"]))
async def change_language(query: types.CallbackQuery, callback_data: dict):
    user_id = query.from_user.id
    user_id = user_data.get(user_id)
    action = callback_data.get("action")
    print(action)
    if action == "en":
        user_data[user_id] = "en"
    if action == "uz":
        user_data[user_id] = "uz"
    if action == "ru":
        user_data[user_id] = "ru"
    await query.answer(text=("language_changed", user_data[user_id]))


@dp.message_handler(state=Button.menu)
async def faq_questions(message: types.Message, state: FSMContext):
    saved_user_language = user_data.get(message.from_user.id, user_language)
    if message.text.lower() == locales.get_locales("faq", saved_user_language).lower():
        await state.set_state(Question.question)
        keyboard_button = types.ReplyKeyboardMarkup(resize_keyboard=True)
        for faqq in faq.faq_questions:
            keyboard_button.add(
                types.KeyboardButton(text=faqq["question"][saved_user_language])
            )
        keyboard_button.add(
            types.KeyboardButton(text=locales.get_locales("back", saved_user_language))
        )
        await message.answer(
            locales.get_locales("faq_questions", lang=saved_user_language),
            reply_markup=keyboard_button,
        )
    if message.text.lower() == locales.get_locales("buy", saved_user_language).lower():
        inline_keyboard = types.InlineKeyboardMarkup(row_width=3)
        inline_keyboard.add(
            types.InlineKeyboardButton(
                text="Buy FinfireProduct",
                url="finfire.uz",
            ),
        )
        await bot.send_photo(
            message.from_user.id,
            photo="https://finfire.uz/logo.png",
            caption_entities=locales.get_locales("about_finfire", saved_user_language),
        )
        await message.answer(
            text=locales.get_locales("about_finfire", saved_user_language),
            reply_markup=inline_keyboard,
            parse_mode="HTML",
        )
    if message.text.lower() == locales.get_locales("lang", saved_user_language).lower():
        inline_keyboard = types.InlineKeyboardMarkup(row_width=3)
        inline_keyboard.add(
            types.InlineKeyboardButton(
                text="English", callback_data=cbd.new(action="en")
            ),
            types.InlineKeyboardButton(
                text="Uzbek", callback_data=cbd.new(action="uz")
            ),
            types.InlineKeyboardButton(
                text="Russian", callback_data=cbd.new(action="ru")
            ),
        )
        await message.answer(
            text=locales.get_locales("lang_command", saved_user_language),
            reply_markup=inline_keyboard,
        )


@dp.message_handler(state=Question.question)
async def faq_answers(message: types.Message, state: FSMContext):
    saved_user_language = user_data.get(message.from_user.id, user_language)
    for faqq in faq.faq_questions:
        if message.text.lower() == faqq["question"][saved_user_language].lower():
            await message.answer(text=faqq["answer"][saved_user_language])
    if message.text.lower() == locales.get_locales("back", saved_user_language).lower():
        await state.set_state(Button.menu)
        saved_user_language = user_data.get(message.from_user.id, user_language)
        kb = [
            [
                types.KeyboardButton(
                    text=locales.get_locales("faq", saved_user_language)
                )
            ],
            [
                types.KeyboardButton(
                    text=locales.get_locales("buy", saved_user_language)
                )
            ],
            [
                types.KeyboardButton(
                    text=locales.get_locales("lang", saved_user_language)
                )
            ],
        ]
        keyboard = types.ReplyKeyboardMarkup(keyboard=kb)
        await message.answer(
            locales.get_locales("menu", saved_user_language), reply_markup=keyboard
        )

cbd = CallbackData("lang", "action")

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)

# //callback_data
