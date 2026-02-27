from sqlalchemy import select, update, delete, func, and_
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional, Any
from datetime import date

from database.models.application import Application
from database.models.enums.application_status import ApplicationStatusEnum, GenderEnum, LevelEnum


class ApplicationRepo:
    """
    High-performance Application repository
    All methods are static for zero instantiation overhead
    """

    __slots__ = ()

    # ==================== CREATE ====================

    @staticmethod
    async def create(session: AsyncSession, user_id: int) -> Application:
        """Create new draft application"""
        app = Application(user_id=user_id, status=ApplicationStatusEnum.draft)
        session.add(app)
        await session.commit()
        await session.refresh(app)
        return app

    @staticmethod
    async def create_full(
            session: AsyncSession,
            user_id: int,
            **kwargs
    ) -> Application:
        """Create application with all fields"""
        app = Application(user_id=user_id, **kwargs)
        session.add(app)
        await session.commit()
        await session.refresh(app)
        return app

    # ==================== READ ====================

    @staticmethod
    async def get(session: AsyncSession, app_id: int) -> Optional[Application]:
        """Get application by ID"""
        return await session.get(Application, app_id)

    @staticmethod
    async def get_by_user(
            session: AsyncSession,
            user_id: int,
            status: Optional[ApplicationStatusEnum] = None
    ) -> list[Application]:
        """Get all applications for user"""
        query = select(Application).where(Application.user_id == user_id)
        if status:
            query = query.where(Application.status == status)
        query = query.order_by(Application.created_at.desc())
        result = await session.execute(query)
        return list(result.scalars().all())

    @staticmethod
    async def get_draft(session: AsyncSession, user_id: int) -> Optional[Application]:
        """Get user's draft application"""
        result = await session.execute(
            select(Application).where(
                Application.user_id == user_id,
                Application.status == ApplicationStatusEnum.draft
            ).limit(1)
        )
        return result.scalar_one_or_none()

    @staticmethod
    async def get_or_create_draft(session: AsyncSession, user_id: int) -> tuple[Application, bool]:
        """Get existing draft or create new one"""
        draft = await ApplicationRepo.get_draft(session, user_id)
        if draft:
            return draft, False

        app = Application(user_id=user_id, status=ApplicationStatusEnum.draft)
        session.add(app)
        await session.commit()
        await session.refresh(app)
        return app, True

    @staticmethod
    async def get_latest(session: AsyncSession, user_id: int) -> Optional[Application]:
        """Get user's latest application"""
        result = await session.execute(
            select(Application)
            .where(Application.user_id == user_id)
            .order_by(Application.created_at.desc())
            .limit(1)
        )
        return result.scalar_one_or_none()

    @staticmethod
    async def get_by_status(
            session: AsyncSession,
            status: ApplicationStatusEnum,
            limit: int = 100,
            offset: int = 0
    ) -> list[Application]:
        """Get applications by status with pagination"""
        result = await session.execute(
            select(Application)
            .where(Application.status == status)
            .order_by(Application.created_at.desc())
            .limit(limit)
            .offset(offset)
        )
        return list(result.scalars().all())

    @staticmethod
    async def get_pending(session: AsyncSession, limit: int = 100) -> list[Application]:
        """Get pending applications"""
        return await ApplicationRepo.get_by_status(session, ApplicationStatusEnum.pending, limit)

    # ==================== FIELD GETTERS ====================

    @staticmethod
    async def get_status(session: AsyncSession, app_id: int) -> Optional[ApplicationStatusEnum]:
        """Get application status"""
        result = await session.execute(
            select(Application.status).where(Application.id == app_id)
        )
        return result.scalar_one_or_none()

    @staticmethod
    async def get_field(session: AsyncSession, app_id: int, field: str) -> Any:
        """Get any single field value"""
        column = getattr(Application, field, None)
        if column is None:
            raise ValueError(f"Unknown field: {field}")
        result = await session.execute(
            select(column).where(Application.id == app_id)
        )
        return result.scalar_one_or_none()

    @staticmethod
    async def get_first_name(session: AsyncSession, app_id: int) -> Optional[str]:
        result = await session.execute(
            select(Application.first_name).where(Application.id == app_id)
        )
        return result.scalar_one_or_none()

    @staticmethod
    async def get_last_name(session: AsyncSession, app_id: int) -> Optional[str]:
        result = await session.execute(
            select(Application.last_name).where(Application.id == app_id)
        )
        return result.scalar_one_or_none()

    @staticmethod
    async def get_full_name(session: AsyncSession, app_id: int) -> Optional[str]:
        result = await session.execute(
            select(Application.first_name, Application.last_name)
            .where(Application.id == app_id)
        )
        row = result.one_or_none()
        if not row:
            return None
        first, last = row
        if first and last:
            return f"{first} {last}"
        return first or ""

    @staticmethod
    async def get_phone(session: AsyncSession, app_id: int) -> Optional[str]:
        result = await session.execute(
            select(Application.phone_number).where(Application.id == app_id)
        )
        return result.scalar_one_or_none()

    @staticmethod
    async def get_photo_path(session: AsyncSession, app_id: int) -> Optional[str]:
        result = await session.execute(
            select(Application.photo_path).where(Application.id == app_id)
        )
        return result.scalar_one_or_none()

    @staticmethod
    async def get_resume_path(session: AsyncSession, app_id: int) -> Optional[str]:
        result = await session.execute(
            select(Application.resume_path).where(Application.id == app_id)
        )
        return result.scalar_one_or_none()

    # ==================== UPDATE ====================

    @staticmethod
    async def update(session: AsyncSession, app_id: int, **kwargs) -> bool:
        """Update application fields"""
        if not kwargs:
            return False
        result = await session.execute(
            update(Application).where(Application.id == app_id).values(**kwargs)
        )
        await session.commit()
        return result.rowcount > 0

    @staticmethod
    async def set_first_name(session: AsyncSession, app_id: int, first_name: str) -> bool:
        result = await session.execute(
            update(Application).where(Application.id == app_id).values(first_name=first_name)
        )
        await session.commit()
        return result.rowcount > 0

    @staticmethod
    async def set_last_name(session: AsyncSession, app_id: int, last_name: str) -> bool:
        result = await session.execute(
            update(Application).where(Application.id == app_id).values(last_name=last_name)
        )
        await session.commit()
        return result.rowcount > 0

    @staticmethod
    async def set_birth_date(session: AsyncSession, app_id: int, birth_date: date) -> bool:
        result = await session.execute(
            update(Application).where(Application.id == app_id).values(birth_date=birth_date)
        )
        await session.commit()
        return result.rowcount > 0

    @staticmethod
    async def set_gender(session: AsyncSession, app_id: int, gender: GenderEnum) -> bool:
        result = await session.execute(
            update(Application).where(Application.id == app_id).values(gender=gender)
        )
        await session.commit()
        return result.rowcount > 0

    @staticmethod
    async def set_address(session: AsyncSession, app_id: int, address: str) -> bool:
        result = await session.execute(
            update(Application).where(Application.id == app_id).values(address=address)
        )
        await session.commit()
        return result.rowcount > 0
    
    @staticmethod
    async def set_additional_courses(session: AsyncSession, app_id: int, additional_courses: bool) -> bool:
        result = await session.execute(
            update(Application).where(Application.id == app_id).values(additional_courses=additional_courses)
        )
        await session.commit()
        return result.rowcount > 0
    
    @staticmethod
    async def set_additional_courses_subject(session: AsyncSession, app_id: int, additional_courses_subject: str) -> bool:
        result = await session.execute(
            update(Application).where(Application.id == app_id).values(additional_courses_subject=additional_courses_subject)
        )
        await session.commit()
        return result.rowcount > 0
    
    @staticmethod
    async def set_marraige_status(session: AsyncSession, app_id: int, marriage_status: bool) -> bool:
        result = await session.execute(
            update(Application).where(Application.id == app_id).values(marriage_status=marriage_status)
        )
        await session.commit()
        return result.rowcount > 0
    
    @staticmethod
    async def set_children_count(session: AsyncSession, app_id: int, children_count: int) -> bool:
        result = await session.execute(
            update(Application).where(Application.id == app_id).values(if_children=children_count)
        )

    @staticmethod
    async def set_phone(session: AsyncSession, app_id: int, phone: str) -> bool:
        result = await session.execute(
            update(Application).where(Application.id == app_id).values(phone_number=phone)
        )
        await session.commit()
        return result.rowcount > 0

    @staticmethod
    async def set_is_student(session: AsyncSession, app_id: int, is_student: bool) -> bool:
        result = await session.execute(
            update(Application).where(Application.id == app_id).values(is_student=is_student)
        )
        await session.commit()
        return result.rowcount > 0

    @staticmethod
    async def set_knowledge_level(session: AsyncSession, app_id: int, level: LevelEnum) -> bool:
        result = await session.execute(
            update(Application).where(Application.id == app_id).values(knowledge_level=level)
        )
        await session.commit()
        return result.rowcount > 0

    @staticmethod
    async def set_russian_level(session: AsyncSession, app_id: int, level: LevelEnum) -> bool:
        result = await session.execute(
            update(Application).where(Application.id == app_id).values(russian_level=level)
        )
        await session.commit()
        return result.rowcount > 0

    @staticmethod
    async def set_russian_voice(session: AsyncSession, app_id: int, path: str) -> bool:
        result = await session.execute(
            update(Application).where(Application.id == app_id).values(russian_voice_path=path)
        )
        await session.commit()
        return result.rowcount > 0

    @staticmethod
    async def set_english_level(session: AsyncSession, app_id: int, level: LevelEnum) -> bool:
        result = await session.execute(
            update(Application).where(Application.id == app_id).values(english_level=level)
        )
        await session.commit()
        return result.rowcount > 0

    @staticmethod
    async def set_english_voice(session: AsyncSession, app_id: int, path: str) -> bool:
        result = await session.execute(
            update(Application).where(Application.id == app_id).values(english_voice_path=path)
        )
        await session.commit()
        return result.rowcount > 0

    @staticmethod
    async def set_work_experience(session: AsyncSession, app_id: int, experience: str) -> bool:
        result = await session.execute(
            update(Application).where(Application.id == app_id).values(work_experience=experience)
        )
        await session.commit()
        return result.rowcount > 0

    @staticmethod
    async def set_last_workplace(session: AsyncSession, app_id: int, workplace: str) -> bool:
        result = await session.execute(
            update(Application).where(Application.id == app_id).values(last_workplace=workplace)
        )
        await session.commit()
        return result.rowcount > 0

    @staticmethod
    async def set_photo(session: AsyncSession, app_id: int, path: str) -> bool:
        result = await session.execute(
            update(Application).where(Application.id == app_id).values(photo_path=path)
        )
        await session.commit()
        return result.rowcount > 0

    @staticmethod
    async def set_resume(session: AsyncSession, app_id: int, path: str) -> bool:
        result = await session.execute(
            update(Application).where(Application.id == app_id).values(resume_path=path)
        )
        await session.commit()
        return result.rowcount > 0

    @staticmethod
    async def set_how_find_out(session: AsyncSession, app_id: int, source: str) -> bool:
        result = await session.execute(
            update(Application).where(Application.id == app_id).values(how_find_out=source)
        )
        await session.commit()
        return result.rowcount > 0

    @staticmethod
    async def set_hr_notes(session: AsyncSession, app_id: int, notes: str) -> bool:
        result = await session.execute(
            update(Application).where(Application.id == app_id).values(hr_notes=notes)
        )
        await session.commit()
        return result.rowcount > 0

    # ==================== STATUS MANAGEMENT ====================

    @staticmethod
    async def set_status(session: AsyncSession, app_id: int, status: ApplicationStatusEnum) -> bool:
        result = await session.execute(
            update(Application).where(Application.id == app_id).values(status=status)
        )
        await session.commit()
        return result.rowcount > 0

    @staticmethod
    async def submit(session: AsyncSession, app_id: int) -> bool:
        """Submit application (draft -> pending)"""
        result = await session.execute(
            update(Application)
            .where(
                Application.id == app_id,
                Application.status == ApplicationStatusEnum.draft
            )
            .values(status=ApplicationStatusEnum.pending)
        )
        await session.commit()
        return result.rowcount > 0

    @staticmethod
    async def start_review(session: AsyncSession, app_id: int) -> bool:
        """Start reviewing (pending -> under_review)"""
        result = await session.execute(
            update(Application)
            .where(
                Application.id == app_id,
                Application.status == ApplicationStatusEnum.pending
            )
            .values(status=ApplicationStatusEnum.under_review)
        )
        await session.commit()
        return result.rowcount > 0

    @staticmethod
    async def schedule_interview(session: AsyncSession, app_id: int) -> bool:
        """Schedule interview"""
        result = await session.execute(
            update(Application)
            .where(
                Application.id == app_id,
                Application.status == ApplicationStatusEnum.under_review
            )
            .values(status=ApplicationStatusEnum.interview_scheduled)
        )
        await session.commit()
        return result.rowcount > 0

    @staticmethod
    async def accept(session: AsyncSession, app_id: int) -> bool:
        """Accept application"""
        result = await session.execute(
            update(Application)
            .where(Application.id == app_id)
            .values(status=ApplicationStatusEnum.accepted)
        )
        await session.commit()
        return result.rowcount > 0

    @staticmethod
    async def reject(session: AsyncSession, app_id: int) -> bool:
        """Reject application"""
        result = await session.execute(
            update(Application)
            .where(Application.id == app_id)
            .values(status=ApplicationStatusEnum.rejected)
        )
        await session.commit()
        return result.rowcount > 0

    @staticmethod
    async def withdraw(session: AsyncSession, app_id: int) -> bool:
        """Withdraw application"""
        result = await session.execute(
            update(Application)
            .where(Application.id == app_id)
            .values(status=ApplicationStatusEnum.withdrawn)
        )
        await session.commit()
        return result.rowcount > 0

    # ==================== DELETE ====================

    @staticmethod
    async def delete(session: AsyncSession, app_id: int) -> bool:
        """Delete application"""
        result = await session.execute(
            delete(Application).where(Application.id == app_id)
        )
        await session.commit()
        return result.rowcount > 0

    @staticmethod
    async def delete_drafts(session: AsyncSession, user_id: int) -> int:
        """Delete all user's draft applications"""
        result = await session.execute(
            delete(Application).where(
                Application.user_id == user_id,
                Application.status == ApplicationStatusEnum.draft
            )
        )
        await session.commit()
        return result.rowcount

    # ==================== STATISTICS ====================

    @staticmethod
    async def count(session: AsyncSession, status: Optional[ApplicationStatusEnum] = None) -> int:
        """Count applications"""
        query = select(func.count(Application.id))
        if status:
            query = query.where(Application.status == status)
        result = await session.execute(query)
        return result.scalar() or 0

    @staticmethod
    async def count_by_user(session: AsyncSession, user_id: int) -> int:
        """Count user's applications"""
        result = await session.execute(
            select(func.count(Application.id)).where(Application.user_id == user_id)
        )
        return result.scalar() or 0

    @staticmethod
    async def count_pending(session: AsyncSession) -> int:
        """Count pending applications"""
        return await ApplicationRepo.count(session, ApplicationStatusEnum.pending)

    @staticmethod
    async def get_stats(session: AsyncSession) -> dict[str, int]:
        """Get application statistics by status"""
        result = await session.execute(
            select(Application.status, func.count(Application.id))
            .group_by(Application.status)
        )
        return {str(row[0].value): row[1] for row in result.all()}