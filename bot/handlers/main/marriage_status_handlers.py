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



router = Router("marriage_status_handlers")


@router.message(ApplicationState.marriage_status, F.text)
async def hande_marriage_status(message: Message, state: FSMContext, user_lang: str = "uz"):
    try:
        user_id = message.from_user.id
        app_id = get_app_id(state)
        lang = await get_lang(state, user_lang)
        
        if is_back(message.text):
            await message.answer(t(lang, 'application.additional_courses.ask'))
            await state.set_state(ApplicationState.additional_courses)
            await DB.user.set_state(user_id, ApplicationState.additional_courses.state)
            return
        
        if is_yes(message.text):
            await DB.app.set_marriage_status(app_id, True)
            await state.update_data(marriage_status=True)
            await state.set_state(ApplicationState.if_children)
            await DB.user.set_state(user_id, ApplicationState.if_children.state)
        elif is_no(message.text):
            await DB.app.set_marriage_status(app_id, False)
            await state.update_data(marriage_status=False)
            await state.set_state(ApplicationState.russian_level)
            await DB.user.set_state(ApplicationState.russian_level.state)
        else:
            await message.answer(t(lang, "application.marriage_status.ask"))
    except Exception as e:
        message.answer(f"Error on marriage handler: {e}")

@router.message(ApplicationState.if_children, F.text)
async def handle_children_count(message: Message, state: FSMContext, user_lang: str = 'uz'):
    try:
        user_id = message.from_user.id
        lang = await get_lang(user_id, user_lang)
        app_id = await get_app_id(state)

        if is_back(message.text):
            await message.answer(t(lang, "application.marriage_status.ask"), reply_markup=Keyboards.back(lang))
            await state.set_state(ApplicationState.marriage_status)
            await DB.user.set_state(user_id, ApplicationState.marriage_status.state)
            return
        
        children_count = message.text
        await DB.app.set_children_count(app_id, children_count)
        await state.update_data(children_count)
        await state.set_state(ApplicationState.russian_level)
        await DB.user.set_state(user_id, ApplicationState.russian_level.state)
    except Exception as e:
        await message.answer(f"Error: {e}")