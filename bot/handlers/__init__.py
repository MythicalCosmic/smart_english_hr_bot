"""
Handler registration
"""
from aiogram import Dispatcher
from bot.handlers import commands, callbacks
from bot.handlers.main import language_selection, menu_handler, settings_handler, personal_info_handler, student_info_handler, work_experience_hander, confirmation_handlers, photo_handlers, last_handlers, marriage_status_handlers, voice_message_handlers

def register_handlers(dp: Dispatcher):
    """Register all handlers"""
    dp.include_router(commands.router)
    dp.include_router(language_selection.router)
    dp.include_router(menu_handler.router)
    dp.include_router(settings_handler.router)
    dp.include_router(personal_info_handler.router)
    dp.include_router(student_info_handler.router)
    dp.include_router(marriage_status_handlers.router)
    dp.include_router(voice_message_handlers.router)
    dp.include_router(work_experience_hander.router)
    dp.include_router(confirmation_handlers.router)
    dp.include_router(photo_handlers.router)
    dp.include_router(last_handlers.router)
    dp.include_router(callbacks.router)
