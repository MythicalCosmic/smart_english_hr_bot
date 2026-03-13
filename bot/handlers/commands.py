from aiogram import Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from services.language_service import t
from bot.keyboards.reply import Keyboards
from bot.states.user import MenuState
from aiogram.fsm.context import FSMContext

router = Router()

@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext, db_user=None, is_new_user: bool = True, user_lang: str = "uz"):
    try:
        if is_new_user or not db_user:
            await message.answer(
                t("uz", "welcome.first_time"),
                reply_markup=Keyboards.language_select()
            )
            await state.set_state(MenuState.language_select)
        elif not  db_user.language_code:
            await message.answer(
                t("uz", "welcome.first_time"),
                reply_markup=Keyboards.language_select()
            )
            await state.set_state(MenuState.language_select)
        else:
            lang = db_user.language_code or "uz"
            await state.update_data(lang=lang)
            await message.answer(
                t(lang, "welcome.returning", name=db_user.first_name or ""),
            )
            await message.answer(
                t(lang, "menu.main"),
                reply_markup=Keyboards.main_menu(lang)
            )
            await state.set_state(MenuState.main)
    except Exception as e:
        print(f"Error in cmd_start: {e}")
        await message.answer(t("uz", "errors.general"))


@router.message(Command("help"))
async def cmd_help(message: Message, state: FSMContext, db_user=None, user_lang: str = "uz"):
    try:
        lang = user_lang
        if db_user and db_user.language_code:
            lang = db_user.language_code
        
        help_text = t(lang, "help.text")
        await message.answer(help_text, reply_markup=Keyboards.main_menu(lang))
        
        dev_text = t(lang, "help.developer")
        await message.answer(dev_text)
        
    except Exception as e:
        print(f"Error in cmd_help: {e}")
        await message.answer(t("uz", "errors.general"))