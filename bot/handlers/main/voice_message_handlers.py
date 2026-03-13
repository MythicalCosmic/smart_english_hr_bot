from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from bot.keyboards.reply import Keyboards
from bot.states.user import ApplicationState
from services.language_service import t
from database.db import DB
from services.language_service import t
from bot.validators.validator import Validators, is_back, is_yes, is_no, get_level
from utils.helpers import get_app_id, get_lang
from services.file_service import FileService
from database.models.enums.application_status import LevelEnum

router = Router(name="voice_message_handlers")


@router.message(ApplicationState.russian_level, F.text)
async def process_russian_level(message: Message, state: FSMContext, user_lang: str = "uz"):
    try:
        lang = await get_lang(state, user_lang)
        user_id = message.from_user.id
        data = await state.get_data()
        
        if is_back(message.text):
            if data.get("marriage_status"):
                await message.answer(t(lang, "application.children_count.ask"), reply_markup=Keyboards.back(lang))
                await state.set_state(ApplicationState.if_children)
                await DB.user.set_state(user_id, ApplicationState.if_children.state)
            else:
                await message.answer(t(lang, "application.marriage_status.ask"), reply_markup=Keyboards.yes_no(lang))
                await state.set_state(ApplicationState.marriage_status)
                await DB.user.set_state(user_id, ApplicationState.marriage_status.state)
            return
        
        level = get_level(message.text)
        if not level:
            await message.answer(t(lang, "application.russian_level.ask"), reply_markup=Keyboards.language_level(lang))
            return
        
        app_id = await get_app_id(state)
        await DB.app.set_russian_level(app_id, LevelEnum(level))
        await message.answer(t(lang, "application.russian_voice.ask"), reply_markup=Keyboards.back(lang))
        await state.set_state(ApplicationState.russian_voice)
    except Exception as e:
        print(f"Error: {e}")



@router.message(ApplicationState.russian_voice, F.voice)
async def process_russian_voice(message: Message, state: FSMContext, user_lang: str = "uz"):
    try:
        lang = await get_lang(state, user_lang)
        app_id = await get_app_id(state)
        
        filepath = await FileService.download_voice(message.bot, message.voice, message.from_user.id, "russian")
        if filepath:
            await DB.app.set_russian_voice(app_id, filepath)
        
        await message.answer(t(lang, "application.english_level.ask"), reply_markup=Keyboards.language_level(lang))
        await state.set_state(ApplicationState.english_level)
    except Exception as e:
        print(f"Error: {e}")


@router.message(ApplicationState.russian_voice, F.text)
async def russian_voice_text(message: Message, state: FSMContext, user_lang: str = "uz"):
    try:
        lang = await get_lang(state, user_lang)
        
        if is_back(message.text):
            await message.answer(t(lang, "application.russian_level.ask"), reply_markup=Keyboards.language_level(lang))
            await state.set_state(ApplicationState.russian_level)
            return
        
        await message.answer(t(lang, "application.russian_voice.invalid"), reply_markup=Keyboards.back(lang))
    except Exception as e:
        print(f"Error: {e}")


@router.message(ApplicationState.english_level, F.text)
async def process_english_level(message: Message, state: FSMContext, user_lang: str = "uz"):
    try:
        lang = await get_lang(state, user_lang)
        
        if is_back(message.text):
            await message.answer(t(lang, "application.russian_voice.ask"), reply_markup=Keyboards.back(lang))
            await state.set_state(ApplicationState.russian_voice)
            return
        
        level = get_level(message.text)
        if not level:
            await message.answer(t(lang, "application.english_level.ask"), reply_markup=Keyboards.language_level(lang))
            return
        
        app_id = await get_app_id(state)
        await DB.app.set_english_level(app_id, LevelEnum(level))
        await message.answer(t(lang, "application.english_voice.ask"), reply_markup=Keyboards.back(lang))
        await state.set_state(ApplicationState.english_voice)
    except Exception as e:
        print(f"Error: {e}")



@router.message(ApplicationState.english_voice, F.voice)
async def process_english_voice(message: Message, state: FSMContext, user_lang: str = "uz"):
    try:
        lang = await get_lang(state, user_lang)
        app_id = await get_app_id(state)
        
        filepath = await FileService.download_voice(message.bot, message.voice, message.from_user.id, "english")
        if filepath:
            await DB.app.set_english_voice(app_id, filepath)
        
        await message.answer(t(lang, "application.has_experience.ask"), reply_markup=Keyboards.yes_no(lang))
        await state.set_state(ApplicationState.has_experience)
    except Exception as e:
        print(f"Error: {e}")


@router.message(ApplicationState.english_voice, F.text)
async def english_voice_text(message: Message, state: FSMContext, user_lang: str = "uz"):
    try:
        lang = await get_lang(state, user_lang)
        
        if is_back(message.text):
            await message.answer(t(lang, "application.english_level.ask"), reply_markup=Keyboards.language_level(lang))
            await state.set_state(ApplicationState.english_level)
            return
        
        await message.answer(t(lang, "application.english_voice.invalid"), reply_markup=Keyboards.back(lang))
    except Exception as e:
        print(f"Error: {e}")