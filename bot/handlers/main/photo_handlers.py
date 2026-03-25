from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from bot.keyboards.reply import Keyboards
from bot.states.user import ApplicationState
from services.language_service import t
from database.db import DB
from bot.validators.validator import is_back, is_skip
from utils.helpers import get_app_id, get_lang
from services.file_service import FileService

router = Router(name="photo_handler")


@router.message(ApplicationState.video_note, F.video_note)
async def process_video_note(message: Message, state: FSMContext, user_lang: str = "uz"):
    try:
        lang = await get_lang(state, user_lang)
        app_id = await get_app_id(state)

        if message.video_note.duration < 30:
            await message.answer(t(lang, "application.video_note.too_short"), reply_markup=Keyboards.back(lang))
            return

        filepath = await FileService.download_video_note(message.bot, message.video_note, message.from_user.id)
        if filepath:
            await DB.app.set_photo(app_id, filepath)

        await message.answer(t(lang, "application.resume.ask"), reply_markup=Keyboards.skip_back(lang))
        await state.set_state(ApplicationState.resume)
    except Exception as e:
        print(f"Error: {e}")


@router.message(ApplicationState.video_note, F.text)
async def video_note_text(message: Message, state: FSMContext, user_lang: str = "uz"):
    try:
        lang = await get_lang(state, user_lang)
        data = await state.get_data()

        if is_back(message.text):
            if data.get("has_experience"):
                await message.answer(t(lang, "application.last_position.ask"), reply_markup=Keyboards.back(lang))
                await state.set_state(ApplicationState.last_position)
            else:
                await message.answer(t(lang, "application.has_experience.ask"), reply_markup=Keyboards.yes_no(lang))
                await state.set_state(ApplicationState.has_experience)
            return

        await message.answer(t(lang, "application.video_note.invalid"), reply_markup=Keyboards.back(lang))
    except Exception as e:
        print(f"Error: {e}")


@router.message(ApplicationState.video_note)
async def video_note_wrong_type(message: Message, state: FSMContext, user_lang: str = "uz"):
    """Catch photos, videos, or other media sent instead of video note"""
    try:
        lang = await get_lang(state, user_lang)
        await message.answer(t(lang, "application.video_note.invalid"), reply_markup=Keyboards.back(lang))
    except Exception as e:
        print(f"Error: {e}")


@router.message(ApplicationState.resume, F.document)
async def process_resume(message: Message, state: FSMContext, user_lang: str = "uz"):
    try:
        lang = await get_lang(state, user_lang)
        app_id = await get_app_id(state)

        doc = message.document
        if doc.file_name and not any(doc.file_name.lower().endswith(ext) for ext in ['.pdf', '.doc', '.docx']):
            await message.answer(t(lang, "application.resume.invalid"), reply_markup=Keyboards.skip_back(lang))
            return

        filepath = await FileService.download_document(message.bot, doc, message.from_user.id)
        if filepath:
            await DB.app.set_resume(app_id, filepath)

        await message.answer(t(lang, "application.how_found.ask"), reply_markup=Keyboards.skip_back(lang))
        await state.set_state(ApplicationState.how_found)
    except Exception as e:
        print(f"Error: {e}")


@router.message(ApplicationState.resume, F.text)
async def resume_text(message: Message, state: FSMContext, user_lang: str = "uz"):
    try:
        lang = await get_lang(state, user_lang)

        if is_back(message.text):
            await message.answer(t(lang, "application.video_note.ask"), reply_markup=Keyboards.back(lang))
            await state.set_state(ApplicationState.video_note)
            return

        if is_skip(message.text):
            await message.answer(t(lang, "application.how_found.ask"), reply_markup=Keyboards.skip_back(lang))
            await state.set_state(ApplicationState.how_found)
            return

        await message.answer(t(lang, "application.resume.invalid"), reply_markup=Keyboards.skip_back(lang))
    except Exception as e:
        print(f"Error: {e}")
