from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from bot.keyboards.reply import Keyboards
from bot.keyboards.inline import get_admin_app_keyboard, get_admin_list_keyboard
from bot.states.user import AdminState, MenuState
from services.language_service import t
from database.db import DB
from core.config import config
from utils.helpers import get_lang

router = Router(name="admin_handler")


def is_admin(user_id: int) -> bool:
    return user_id in config.admin_ids


@router.message(Command("admin"))
async def cmd_admin(message: Message, state: FSMContext, user_lang: str = "uz"):
    if not is_admin(message.from_user.id):
        await message.answer(t(user_lang, "admin.no_access"))
        return

    lang = await get_lang(state, user_lang)
    await state.update_data(lang=lang)
    await message.answer(t(lang, "admin.menu"), reply_markup=Keyboards.admin_menu(lang))
    await state.set_state(AdminState.main)


@router.message(AdminState.main, F.text)
async def admin_menu_handler(message: Message, state: FSMContext, user_lang: str = "uz"):
    if not is_admin(message.from_user.id):
        return

    lang = await get_lang(state, user_lang)
    text = message.text.lower()

    if "stat" in text or "📊" in text:
        await show_stats(message, lang)
    elif "pending" in text or "kutilayotgan" in text or "ожидающ" in text or "⏳" in text:
        await show_pending(message, lang)
    elif "back" in text or "orqaga" in text or "назад" in text or "⬅" in text:
        await message.answer(t(lang, "menu.main"), reply_markup=Keyboards.main_menu(lang))
        await state.set_state(MenuState.main)
    else:
        await message.answer(t(lang, "admin.menu"), reply_markup=Keyboards.admin_menu(lang))


async def show_stats(message: Message, lang: str):
    try:
        stats = await DB.app.get_stats()
        users = await DB.user.count()

        await message.answer(t(lang, "admin.stats",
            total=sum(stats.values()),
            pending=stats.get("pending", 0),
            under_review=stats.get("under_review", 0),
            interview=stats.get("interview_scheduled", 0),
            accepted=stats.get("accepted", 0),
            rejected=stats.get("rejected", 0),
            users=users
        ))
    except Exception as e:
        print(f"Error in show_stats: {e}")
        await message.answer(t(lang, "errors.general"))


async def show_pending(message: Message, lang: str):
    try:
        apps = await DB.app.get_pending(limit=20)

        if not apps:
            await message.answer(t(lang, "admin.no_pending"))
            return

        await message.answer(t(lang, "admin.app_list_header"))

        for app in apps:
            name = f"{app.first_name or '—'} {app.last_name or '—'}"
            phone = app.phone_number or "—"
            text = f"#{app.id} | {name} | {phone}"
            await message.answer(text, reply_markup=get_admin_list_keyboard(app.id))
    except Exception as e:
        print(f"Error in show_pending: {e}")
        await message.answer(t(lang, "errors.general"))


@router.callback_query(F.data.startswith("admin_view_"))
async def cb_view_app(callback: CallbackQuery, state: FSMContext, user_lang: str = "uz"):
    if not is_admin(callback.from_user.id):
        await callback.answer("No access")
        return

    lang = await get_lang(state, user_lang)
    app_id = int(callback.data.split("_")[-1])

    try:
        app = await DB.app.get(app_id)
        if not app:
            await callback.answer("Application not found")
            return

        def _val(field):
            return field.value if hasattr(field, "value") else (field or "—")

        await callback.message.answer(t(lang, "admin.app_detail",
            app_id=app.id,
            first_name=app.first_name or "—",
            last_name=app.last_name or "—",
            birth_date=app.birth_date.strftime("%d.%m.%Y") if app.birth_date else "—",
            phone=app.phone_number or "—",
            email=app.email or "—",
            is_student="Yes" if app.is_student else "No",
            education_level=_val(app.education_level),
            russian_level=_val(app.russian_level),
            english_level=_val(app.english_level),
            has_experience="Yes" if app.has_work_experience else "No",
            workplace=app.last_workplace or "—",
            status=_val(app.status)
        ), reply_markup=get_admin_app_keyboard(app.id))

        from pathlib import Path
        from aiogram.types import FSInputFile

        if app.photo_path and Path(app.photo_path).exists():
            try:
                await callback.message.answer_photo(FSInputFile(app.photo_path))
            except:
                pass

        if app.resume_path and Path(app.resume_path).exists():
            try:
                await callback.message.answer_document(FSInputFile(app.resume_path))
            except:
                pass

        if app.russian_voice_path and Path(app.russian_voice_path).exists():
            try:
                await callback.message.answer_voice(FSInputFile(app.russian_voice_path), caption="🇷🇺 Russian voice")
            except:
                pass

        if app.english_voice_path and Path(app.english_voice_path).exists():
            try:
                await callback.message.answer_voice(FSInputFile(app.english_voice_path), caption="🇬🇧 English voice")
            except:
                pass

        await callback.answer()
        await state.update_data(viewing_app_id=app.id)
        await state.set_state(AdminState.viewing_app)
    except Exception as e:
        print(f"Error in cb_view_app: {e}")
        await callback.answer("Error")


@router.callback_query(F.data.startswith("admin_accept_"))
async def cb_accept_app(callback: CallbackQuery, state: FSMContext, user_lang: str = "uz"):
    if not is_admin(callback.from_user.id):
        await callback.answer("No access")
        return

    lang = await get_lang(state, user_lang)
    app_id = int(callback.data.split("_")[-1])

    try:
        app = await DB.app.get(app_id)
        if not app:
            await callback.answer("Not found")
            return

        await DB.app.accept(app_id)
        await callback.message.answer(t(lang, "admin.accepted", app_id=app_id))
        await callback.answer()

        try:
            await callback.bot.send_message(
                app.user_id,
                t(lang, "admin.applicant_accepted")
            )
        except:
            pass

        await state.set_state(AdminState.main)
    except Exception as e:
        print(f"Error in cb_accept_app: {e}")
        await callback.answer("Error")


@router.callback_query(F.data.startswith("admin_reject_"))
async def cb_reject_app(callback: CallbackQuery, state: FSMContext, user_lang: str = "uz"):
    if not is_admin(callback.from_user.id):
        await callback.answer("No access")
        return

    lang = await get_lang(state, user_lang)
    app_id = int(callback.data.split("_")[-1])

    try:
        app = await DB.app.get(app_id)
        if not app:
            await callback.answer("Not found")
            return

        await DB.app.reject(app_id)
        await callback.message.answer(t(lang, "admin.rejected", app_id=app_id))
        await callback.answer()

        try:
            await callback.bot.send_message(
                app.user_id,
                t(lang, "admin.applicant_rejected")
            )
        except:
            pass

        await state.set_state(AdminState.main)
    except Exception as e:
        print(f"Error in cb_reject_app: {e}")
        await callback.answer("Error")


@router.callback_query(F.data.startswith("admin_note_"))
async def cb_add_note(callback: CallbackQuery, state: FSMContext, user_lang: str = "uz"):
    if not is_admin(callback.from_user.id):
        await callback.answer("No access")
        return

    lang = await get_lang(state, user_lang)
    app_id = int(callback.data.split("_")[-1])

    await state.update_data(noting_app_id=app_id)
    await callback.message.answer(t(lang, "admin.note_ask"))
    await callback.answer()
    await state.set_state(AdminState.adding_note)


@router.message(AdminState.adding_note, F.text)
async def process_admin_note(message: Message, state: FSMContext, user_lang: str = "uz"):
    if not is_admin(message.from_user.id):
        return

    lang = await get_lang(state, user_lang)
    data = await state.get_data()
    app_id = data.get("noting_app_id")

    if not app_id:
        await message.answer(t(lang, "errors.general"))
        await state.set_state(AdminState.main)
        return

    try:
        await DB.app.update(app_id, hr_notes=message.text[:500])
        await message.answer(t(lang, "admin.note_saved"), reply_markup=Keyboards.admin_menu(lang))
        await state.set_state(AdminState.main)
    except Exception as e:
        print(f"Error in process_admin_note: {e}")
        await message.answer(t(lang, "errors.general"))
