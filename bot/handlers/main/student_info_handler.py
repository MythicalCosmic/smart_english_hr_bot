from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from bot.keyboards.reply import Keyboards
from bot.states.user import ApplicationState
from services.language_service import t
from database.db import DB
from services.language_service import t
from bot.validators.validator import Validators, get_level, is_yes, is_back, is_no
from utils.helpers import get_app_id, get_lang
from utils.helpers import get_lang

router = Router(name="student_info_handler")



@router.message(ApplicationState.is_student, F.text)
async def process_is_student(message: Message, state: FSMContext, user_lang: str = "uz"):
    try:
        lang = await get_lang(state, user_lang)
        
        if is_back(message.text):
            await message.answer(t(lang, "application.email.ask"), reply_markup=Keyboards.skip_back(lang))
            await state.set_state(ApplicationState.email)
            await DB.user.set_state(message.from_user.id, ApplicationState.email.state)
            return
        
        app_id = await get_app_id(state)
        
        if is_yes(message.text):
            await DB.app.set_is_student(app_id, True)
            await state.update_data(is_student=True)
            await message.answer(t(lang, "application.education_place.ask"), reply_markup=Keyboards.back(lang))
            await state.set_state(ApplicationState.education_place)
            await DB.user.set_state(message.from_user.id, ApplicationState.education_place.state)
        elif is_no(message.text):
            await DB.app.set_is_student(app_id, False)
            await state.update_data(is_student=False)
            await message.answer(t(lang, "application.additional_courses.ask"), reply_markup=Keyboards.yes_no(lang))
            await state.set_state(ApplicationState.additional_courses)
            await DB.user.set_state(message.from_user.id, ApplicationState.additional_courses.state)
        else:
            await message.answer(t(lang, "application.is_student.ask"), reply_markup=Keyboards.yes_no(lang))
    except Exception as e:
        print(f"Error: {e}")


@router.message(ApplicationState.education_place, F.text)
async def process_education_place(message: Message, state: FSMContext, user_lang: str = "uz"):
    try:
        lang = await get_lang(state, user_lang)
        
        if is_back(message.text):
            await message.answer(t(lang, "application.is_student.ask"), reply_markup=Keyboards.yes_no(lang))
            await state.set_state(ApplicationState.is_student)
            await DB.user.set_state(message.from_user.id, ApplicationState.is_student.state)
            return
        
        is_valid, cleaned = Validators.text_field(message.text)
        
        if not is_valid:
            await message.answer(t(lang, "application.education_place.invalid"), reply_markup=Keyboards.back(lang))
            return
        
        app_id = await get_app_id(state)
        await DB.app.update(app_id, education_place=cleaned)
        await message.answer(t(lang, "application.education_level.ask"), reply_markup=Keyboards.language_level(lang))
        await state.set_state(ApplicationState.education_level)
        await DB.user.set_state(message.from_user.id, ApplicationState.education_level.state)
    except Exception as e:
        print(f"Error: {e}")


@router.message(ApplicationState.education_level, F.text)
async def process_education_level(message: Message, state: FSMContext, user_lang: str = "uz"):
    try:
        lang = await get_lang(state, user_lang)
        
        if is_back(message.text):
            await message.answer(t(lang, "application.education_place.ask"), reply_markup=Keyboards.back(lang))
            await state.set_state(ApplicationState.education_place)
            await DB.user.set_state(message.from_user.id, ApplicationState.education_place.state)
            return
        
        level = get_level(message.text)
        if not level:
            await message.answer(t(lang, "application.education_level.ask"), reply_markup=Keyboards.language_level(lang))
            return
        
        app_id = await get_app_id(state)
        from database.models.enums.application_status import LevelEnum
        await DB.app.update(app_id, education_level=LevelEnum(level))
        await message.answer(t(lang, "application.additional_courses.ask"), reply_markup=Keyboards.yes_no(lang))
        await state.set_state(ApplicationState.additional_courses)
        await DB.user.set_state(message.from_user.id, ApplicationState.additional_courses.state)
    except Exception as e:
        print(f"Error: {e}")

@router.message(ApplicationState.additional_courses, F.text)
async def proccess_additional_courses(message: Message, state: FSMContext, user_lang: str = 'uz'):
    try:
        lang = await get_lang(state, user_lang)
        app_id = get_app_id(state)

        if is_back(message.text):
            await message.answer(t(lang, "application.education_level.ask"), reply_markup=Keyboards.back(lang))
            await state.set_state(ApplicationState.education_level)
            await DB.user.set_state(message.from_user.id, ApplicationState.education_level.state)
            return
        
        if is_yes(message.text):
            await DB.app.set_additional_courses(app_id, True)
            await state.update_data(additional_courses=True)
            await message.answer(t(lang, "application.additional_courses_subject.ask"), reply_markup=Keyboards.back(lang))
            await state.set_state(ApplicationState.additional_courses_subject)
            await DB.user.set_state(message.from_user.id, ApplicationState.additional_courses_subject.state)
        elif is_no(message.text):
            await DB.app.set_additional_courses(app_id, False)
            await state.update_data(additional_courses=False)
            await message.answer(t(lang, "application.marriage_status.ask"), reply_markup=Keyboards.yes_no(lang))
            await state.set_state(ApplicationState.marriage_status)
            await DB.user.set_state(message.from_user.id, ApplicationState.marriage_status.state)
        else:
            await message.answer(t(lang, "application.additional_courses.ask"), reply_markup=Keyboards.yes_no(lang))
    except Exception as e:
        print(f'Error: {e}')

@router.message(ApplicationState.additional_courses_subject, F.text)
async def proccess_additional_courses_subject(message: Message, state: FSMContext, user_lang: str = "uz"):
    try:

        lang = await get_lang(state, user_lang)
        if is_back(message.text):
            await message.answer(t(lang, "application.additional_courses.ask"), reply_markup=Keyboards.yes_no(lang))
            await state.set_state(ApplicationState.additional_courses)
            await DB.user.set_state(message.from_user.id, ApplicationState.additional_courses.state)
            
        user_id = message.from_user.id
        app_id =  await get_app_id(state)
        course_subject = message.text
        if len(course_subject) < 3:
            message.answer(t(lang, 'application.additional_courses.ask'), reply_markup=Keyboards.back(lang))
        await DB.app.set_additional_courses_subject(app_id, course_subject)
        await state.update_data(course_subject=course_subject)
        await state.set_state(ApplicationState.marriage_status)
        await DB.user.set_state(user_id, ApplicationState.marriage_status.state)
    except Exception as e:
        print(f"Error: {e}")
