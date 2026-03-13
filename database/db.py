"""
🚀 LIGHTNING FAST Database Facade
One import, all operations
"""
from typing import Optional, Any
from datetime import date

from database.config import async_session
from database.repositories.user_repository import UserRepo
from database.repositories.application_repository import ApplicationRepo
from database.models.enums.application_status import ApplicationStatusEnum, GenderEnum, LevelEnum


class DB:
    """
    Ultra-fast database facade

    Usage:
        await DB.user.get_state(user_id)
        await DB.app.set_first_name(app_id, "John")
    """

    class user:
        """User operations"""

        # ===== CREATE =====
        @staticmethod
        async def create(user_id: int, first_name: str, last_name: str = None, username: str = None):
            async with async_session() as s:
                return await UserRepo.create(s, user_id, first_name, last_name, username)

        @staticmethod
        async def get_or_create(user_id: int, first_name: str, last_name: str = None, username: str = None):
            async with async_session() as s:
                return await UserRepo.get_or_create(s, user_id, first_name, last_name, username)

        # ===== READ =====
        @staticmethod
        async def get(user_id: int):
            async with async_session() as s:
                return await UserRepo.get(s, user_id)

        @staticmethod
        async def exists(user_id: int) -> bool:
            async with async_session() as s:
                return await UserRepo.exists(s, user_id)

        @staticmethod
        async def get_username(user_id: int) -> Optional[str]:
            async with async_session() as s:
                return await UserRepo.get_username(s, user_id)

        @staticmethod
        async def get_first_name(user_id: int) -> Optional[str]:
            async with async_session() as s:
                return await UserRepo.get_first_name(s, user_id)

        @staticmethod
        async def get_last_name(user_id: int) -> Optional[str]:
            async with async_session() as s:
                return await UserRepo.get_last_name(s, user_id)

        @staticmethod
        async def get_full_name(user_id: int) -> Optional[str]:
            async with async_session() as s:
                return await UserRepo.get_full_name(s, user_id)

        @staticmethod
        async def get_language(user_id: int) -> Optional[str]:
            async with async_session() as s:
                return await UserRepo.get_language(s, user_id)

        @staticmethod
        async def is_admin(user_id: int) -> bool:
            async with async_session() as s:
                return await UserRepo.is_admin(s, user_id)

        @staticmethod
        async def is_hr(user_id: int) -> bool:
            async with async_session() as s:
                return await UserRepo.is_hr(s, user_id)

        @staticmethod
        async def is_active(user_id: int) -> bool:
            async with async_session() as s:
                return await UserRepo.is_active(s, user_id)

        @staticmethod
        async def is_blocked(user_id: int) -> bool:
            async with async_session() as s:
                return await UserRepo.is_blocked(s, user_id)

        # ===== STATE =====
        @staticmethod
        async def get_state(user_id: int) -> Optional[str]:
            async with async_session() as s:
                return await UserRepo.get_state(s, user_id)

        @staticmethod
        async def get_state_data(user_id: int) -> Optional[dict]:
            async with async_session() as s:
                return await UserRepo.get_state_data(s, user_id)

        @staticmethod
        async def get_state_with_data(user_id: int) -> tuple[Optional[str], Optional[dict]]:
            async with async_session() as s:
                return await UserRepo.get_state_with_data(s, user_id)

        @staticmethod
        async def set_state(user_id: int, state: str, state_data: dict = None) -> bool:
            async with async_session() as s:
                return await UserRepo.set_state(s, user_id, state, state_data)

        @staticmethod
        async def update_state_data(user_id: int, **kwargs) -> bool:
            async with async_session() as s:
                return await UserRepo.update_state_data(s, user_id, **kwargs)

        @staticmethod
        async def clear_state(user_id: int) -> bool:
            async with async_session() as s:
                return await UserRepo.clear_state(s, user_id)

        # ===== UPDATE =====
        @staticmethod
        async def update(user_id: int, **kwargs) -> bool:
            async with async_session() as s:
                return await UserRepo.update(s, user_id, **kwargs)

        @staticmethod
        async def set_first_name(user_id: int, first_name: str) -> bool:
            async with async_session() as s:
                return await UserRepo.set_first_name(s, user_id, first_name)

        @staticmethod
        async def set_last_name(user_id: int, last_name: str) -> bool:
            async with async_session() as s:
                return await UserRepo.set_last_name(s, user_id, last_name)

        @staticmethod
        async def set_username(user_id: int, username: str) -> bool:
            async with async_session() as s:
                return await UserRepo.set_username(s, user_id, username)

        @staticmethod
        async def set_language(user_id: int, language: str) -> bool:
            async with async_session() as s:
                return await UserRepo.set_language(s, user_id, language)


        @staticmethod
        async def set_blocked(user_id: int, blocked: bool) -> bool:
            async with async_session() as s:
                return await UserRepo.set_blocked(s, user_id, blocked)

        @staticmethod
        async def sync_telegram(user_id: int, first_name: str, last_name: str = None, username: str = None) -> bool:
            async with async_session() as s:
                return await UserRepo.sync_telegram_data(s, user_id, first_name, last_name, username)
            

        # ===== DELETE =====
        @staticmethod
        async def delete(user_id: int) -> bool:
            async with async_session() as s:
                return await UserRepo.delete(s, user_id)

        # ===== LISTS =====
        @staticmethod
        async def get_admins():
            async with async_session() as s:
                return await UserRepo.get_admins(s)

        @staticmethod
        async def get_all_ids(active_only: bool = True) -> list[int]:
            async with async_session() as s:
                return await UserRepo.get_all_ids(s, active_only)

        @staticmethod
        async def count(active_only: bool = True) -> int:
            async with async_session() as s:
                return await UserRepo.count(s, active_only)

    class app:
        """Application operations"""

        # ===== CREATE =====
        @staticmethod
        async def create(user_id: int):
            async with async_session() as s:
                return await ApplicationRepo.create(s, user_id)

        @staticmethod
        async def get_or_create_draft(user_id: int):
            async with async_session() as s:
                return await ApplicationRepo.get_or_create_draft(s, user_id)

        # ===== READ =====
        @staticmethod
        async def get(app_id: int):
            async with async_session() as s:
                return await ApplicationRepo.get(s, app_id)

        @staticmethod
        async def get_by_user(user_id: int, status: ApplicationStatusEnum = None):
            async with async_session() as s:
                return await ApplicationRepo.get_by_user(s, user_id, status)

        @staticmethod
        async def get_draft(user_id: int):
            async with async_session() as s:
                return await ApplicationRepo.get_draft(s, user_id)

        @staticmethod
        async def get_latest(user_id: int):
            async with async_session() as s:
                return await ApplicationRepo.get_latest(s, user_id)

        @staticmethod
        async def get_pending(limit: int = 100):
            async with async_session() as s:
                return await ApplicationRepo.get_pending(s, limit)

        @staticmethod
        async def get_status(app_id: int) -> Optional[ApplicationStatusEnum]:
            async with async_session() as s:
                return await ApplicationRepo.get_status(s, app_id)

        @staticmethod
        async def get_full_name(app_id: int) -> Optional[str]:
            async with async_session() as s:
                return await ApplicationRepo.get_full_name(s, app_id)

        @staticmethod
        async def get_phone(app_id: int) -> Optional[str]:
            async with async_session() as s:
                return await ApplicationRepo.get_phone(s, app_id)

        # ===== UPDATE =====
        @staticmethod
        async def update(app_id: int, **kwargs) -> bool:
            async with async_session() as s:
                return await ApplicationRepo.update(s, app_id, **kwargs)

        @staticmethod
        async def set_first_name(app_id: int, name: str) -> bool:
            async with async_session() as s:
                return await ApplicationRepo.set_first_name(s, app_id, name)

        @staticmethod
        async def set_last_name(app_id: int, name: str) -> bool:
            async with async_session() as s:
                return await ApplicationRepo.set_last_name(s, app_id, name)

        @staticmethod
        async def set_birth_date(app_id: int, birth_date: date) -> bool:
            async with async_session() as s:
                return await ApplicationRepo.set_birth_date(s, app_id, birth_date)

        @staticmethod
        async def set_gender(app_id: int, gender: GenderEnum) -> bool:
            async with async_session() as s:
                return await ApplicationRepo.set_gender(s, app_id, gender)

        @staticmethod
        async def set_address(app_id: int, address: str) -> bool:
            async with async_session() as s:
                return await ApplicationRepo.set_address(s, app_id, address)
            
        @staticmethod
        async def set_additional_courses(app_id: int, additional_courses: bool) -> bool:
            async with async_session() as s:
                return await ApplicationRepo.set_additional_courses(s, app_id, additional_courses)

        @staticmethod
        async def set_additional_courses_subject(app_id: int, additional_course_subject: str) -> bool:
            async with async_session() as s:
                return await ApplicationRepo.set_additional_courses_subject(s, app_id, additional_course_subject)

        @staticmethod
        async def set_marriage_status(app_id: int, marriage_status: bool) -> bool:
            async with async_session() as s:
                return await ApplicationRepo.set_marriage_status(s, app_id, marriage_status)

        @staticmethod
        async def set_children_count(app_id: int, children_count: str) -> bool:
            async with async_session() as s:
                return await ApplicationRepo.set_children_count(s, app_id, children_count)
            

        @staticmethod
        async def set_phone(app_id: int, phone: str) -> bool:
            async with async_session() as s:
                return await ApplicationRepo.set_phone(s, app_id, phone)

        @staticmethod
        async def set_photo(app_id: int, path: str) -> bool:
            async with async_session() as s:
                return await ApplicationRepo.set_photo(s, app_id, path)
            
        @staticmethod
        async def set_is_student(user_id: int, is_student: bool) -> bool:
            async with async_session() as s:
                return await ApplicationRepo.set_is_student(s, user_id, is_student)

        @staticmethod
        async def set_resume(app_id: int, path: str) -> bool:
            async with async_session() as s:
                return await ApplicationRepo.set_resume(s, app_id, path)

        @staticmethod
        async def set_russian_level(app_id: int, level: LevelEnum) -> bool:
            async with async_session() as s:
                return await ApplicationRepo.set_russian_level(s, app_id, level)

        @staticmethod
        async def set_english_level(app_id: int, level: LevelEnum) -> bool:
            async with async_session() as s:
                return await ApplicationRepo.set_english_level(s, app_id, level)

        @staticmethod
        async def set_russian_voice(app_id: int, path: str) -> bool:
            async with async_session() as s:
                return await ApplicationRepo.set_russian_voice(s, app_id, path)

        @staticmethod
        async def set_english_voice(app_id: int, path: str) -> bool:
            async with async_session() as s:
                return await ApplicationRepo.set_english_voice(s, app_id, path)

        # ===== STATUS =====
        @staticmethod
        async def submit(app_id: int) -> bool:
            async with async_session() as s:
                return await ApplicationRepo.submit(s, app_id)

        @staticmethod
        async def accept(app_id: int) -> bool:
            async with async_session() as s:
                return await ApplicationRepo.accept(s, app_id)

        @staticmethod
        async def reject(app_id: int) -> bool:
            async with async_session() as s:
                return await ApplicationRepo.reject(s, app_id)

        @staticmethod
        async def withdraw(app_id: int) -> bool:
            async with async_session() as s:
                return await ApplicationRepo.withdraw(s, app_id)

        # ===== DELETE =====
        @staticmethod
        async def delete(app_id: int) -> bool:
            async with async_session() as s:
                return await ApplicationRepo.delete(s, app_id)

        @staticmethod
        async def delete_drafts(user_id: int) -> int:
            async with async_session() as s:
                return await ApplicationRepo.delete_drafts(s, user_id)

        # ===== STATS =====
        @staticmethod
        async def count(status: ApplicationStatusEnum = None) -> int:
            async with async_session() as s:
                return await ApplicationRepo.count(s, status)

        @staticmethod
        async def count_pending() -> int:
            async with async_session() as s:
                return await ApplicationRepo.count_pending(s)

        @staticmethod
        async def get_stats() -> dict[str, int]:
            async with async_session() as s:
                return await ApplicationRepo.get_stats(s)