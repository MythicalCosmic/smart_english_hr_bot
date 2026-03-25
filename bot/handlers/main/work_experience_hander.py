from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from bot.keyboards.reply import Keyboards
from bot.states.user import ApplicationState
from services.language_service import t
from database.db import DB
from services.language_service import t
from bot.validators.validator import Validators, is_back, is_yes, is_no
from utils.helpers import get_app_id, get_lang


router = Router(name="work_experience_handler")


@router.message(ApplicationState.has_experience, F.text)
async def process_has_experience(message: Message, state: FSMContext, user_lang: str = "uz"):
    try:
        lang = await get_lang(state, user_lang)
        
        if is_back(message.text):
            await message.answer(t(lang, "application.english_voice.ask"), reply_markup=Keyboards.back(lang))
            await state.set_state(ApplicationState.english_voice)
            await DB.user.set_state(message.from_user.id, ApplicationState.english_voice.state)
            return
        
        app_id = await get_app_id(state)
        
        if is_yes(message.text):
            await DB.app.update(app_id, has_work_experience=True)
            await state.update_data(has_experience=True)
            await message.answer(t(lang, "application.experience_years.ask"), reply_markup=Keyboards.back(lang))
            await state.set_state(ApplicationState.experience_years)
        elif is_no(message.text):
            await DB.app.update(app_id, has_work_experience=False)
            await state.update_data(has_experience=False)
            await message.answer(t(lang, "application.video_note.ask"), reply_markup=Keyboards.back(lang))
            await state.set_state(ApplicationState.video_note)
        else:
            await message.answer(t(lang, "application.has_experience.ask"), reply_markup=Keyboards.yes_no(lang))
    except Exception as e:
        print(f"Error: {e}")


@router.message(ApplicationState.experience_years, F.text)
async def process_experience_years(message: Message, state: FSMContext, user_lang: str = "uz"):
    try:
        lang = await get_lang(state, user_lang)
        
        if is_back(message.text):
            await message.answer(t(lang, "application.has_experience.ask"), reply_markup=Keyboards.yes_no(lang))
            await state.set_state(ApplicationState.has_experience)
            return
        
        is_valid, years = Validators.experience_years(message.text)
        if not is_valid:
            await message.answer(t(lang, "application.experience_years.invalid"), reply_markup=Keyboards.back(lang))
            return
        
        app_id = await get_app_id(state)
        await DB.app.update(app_id, work_experience_lenght=years)
        await state.update_data(experience_years=years)
        await message.answer(t(lang, "application.last_workplace.ask"), reply_markup=Keyboards.back(lang))
        await state.set_state(ApplicationState.last_workplace)
    except Exception as e:
        print(f"Error: {e}")


@router.message(ApplicationState.last_workplace, F.text)
async def process_last_workplace(message: Message, state: FSMContext, user_lang: str = "uz"):
    try:
        lang = await get_lang(state, user_lang)
        
        if is_back(message.text):
            await message.answer(t(lang, "application.experience_years.ask"), reply_markup=Keyboards.back(lang))
            await state.set_state(ApplicationState.experience_years)
            return
        
        is_valid, cleaned = Validators.text_field(message.text)
        if not is_valid:
            await message.answer(t(lang, "application.last_workplace.invalid"), reply_markup=Keyboards.back(lang))
            return
        
        app_id = await get_app_id(state)
        await DB.app.update(app_id, last_workplace=cleaned)
        await message.answer(t(lang, "application.last_position.ask"), reply_markup=Keyboards.back(lang))
        await state.set_state(ApplicationState.last_position)
    except Exception as e:
        print(f"Error: {e}")


@router.message(ApplicationState.last_position, F.text)
async def process_last_position(message: Message, state: FSMContext, user_lang: str = "uz"):
    try:
        lang = await get_lang(state, user_lang)
        
        if is_back(message.text):
            await message.answer(t(lang, "application.last_workplace.ask"), reply_markup=Keyboards.back(lang))
            await state.set_state(ApplicationState.last_workplace)
            return
        
        is_valid, cleaned = Validators.text_field(message.text, 2, 100)
        if not is_valid:
            await message.answer(t(lang, "application.last_position.invalid"), reply_markup=Keyboards.back(lang))
            return
        
        app_id = await get_app_id(state)
        await DB.app.update(app_id, last_position=cleaned)
        await message.answer(t(lang, "application.video_note.ask"), reply_markup=Keyboards.back(lang))
        await state.set_state(ApplicationState.video_note)
    except Exception as e:
        print(f"Error: {e}")