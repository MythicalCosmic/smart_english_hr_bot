"""
🎹 Fixed Keyboard Builders
"""
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from services.language_service import btn


class Keyboards:
    """Keyboard builder with proper language support"""
    
    @staticmethod
    def remove() -> ReplyKeyboardRemove:
        return ReplyKeyboardRemove()
    
    @staticmethod
    def language_select() -> ReplyKeyboardMarkup:
        """Language selection - always same buttons"""
        builder = ReplyKeyboardBuilder()
        builder.row(
            KeyboardButton(text="🇺🇿 O'zbekcha"),
            KeyboardButton(text="🇷🇺 Русский"),
            KeyboardButton(text="🇬🇧 English")
        )
        return builder.as_markup(resize_keyboard=True)
    
    @staticmethod
    def main_menu(lang: str) -> ReplyKeyboardMarkup:
        """Main menu"""
        builder = ReplyKeyboardBuilder()
        builder.row(KeyboardButton(text=btn(lang, "start_application")))
        builder.row(KeyboardButton(text=btn(lang, "settings")))
        return builder.as_markup(resize_keyboard=True)
    
    @staticmethod
    def settings(lang: str) -> ReplyKeyboardMarkup:
        """Settings with language options"""
        builder = ReplyKeyboardBuilder()
        builder.row(
            KeyboardButton(text="🇺🇿 O'zbekcha"),
            KeyboardButton(text="🇷🇺 Русский"),
            KeyboardButton(text="🇬🇧 English")
        )
        builder.row(KeyboardButton(text=btn(lang, "back")))
        return builder.as_markup(resize_keyboard=True)
    
    @staticmethod
    def back(lang: str) -> ReplyKeyboardMarkup:
        """Back button only"""
        builder = ReplyKeyboardBuilder()
        builder.row(KeyboardButton(text=btn(lang, "back")))
        return builder.as_markup(resize_keyboard=True)
    
    @staticmethod
    def skip_back(lang: str) -> ReplyKeyboardMarkup:
        """Skip and back buttons"""
        builder = ReplyKeyboardBuilder()
        builder.row(
            KeyboardButton(text=btn(lang, "skip")),
            KeyboardButton(text=btn(lang, "back"))
        )
        return builder.as_markup(resize_keyboard=True)
    
    @staticmethod
    def gender(lang: str) -> ReplyKeyboardMarkup:
        """Gender selection"""
        builder = ReplyKeyboardBuilder()
        builder.row(
            KeyboardButton(text=btn(lang, "male")),
            KeyboardButton(text=btn(lang, "female"))
        )
        builder.row(KeyboardButton(text=btn(lang, "back")))
        return builder.as_markup(resize_keyboard=True)
    
    @staticmethod
    def yes_no(lang: str) -> ReplyKeyboardMarkup:
        """Yes/No selection"""
        builder = ReplyKeyboardBuilder()
        builder.row(
            KeyboardButton(text=btn(lang, "yes")),
            KeyboardButton(text=btn(lang, "no"))
        )
        builder.row(KeyboardButton(text=btn(lang, "back")))
        return builder.as_markup(resize_keyboard=True)
    
    @staticmethod
    def phone(lang: str) -> ReplyKeyboardMarkup:
        """Phone with contact button"""
        builder = ReplyKeyboardBuilder()
        builder.row(KeyboardButton(text=btn(lang, "send_phone"), request_contact=True))
        builder.row(KeyboardButton(text=btn(lang, "back")))
        return builder.as_markup(resize_keyboard=True)
    
    @staticmethod
    def language_level(lang: str) -> ReplyKeyboardMarkup:
        """Language proficiency levels"""
        builder = ReplyKeyboardBuilder()
        builder.row(
            KeyboardButton(text=btn(lang, "secondary")),
            KeyboardButton(text=btn(lang, "specialized_secondary"))
        )
        builder.row(
            KeyboardButton(text=btn(lang, "incomplete_higher")),
            KeyboardButton(text=btn(lang, "bachelor"))
        )
        builder.row(
            KeyboardButton(text=btn(lang, "master"))
        )
        builder.row(
            KeyboardButton(text=btn(lang, "back"))
        )
        return builder.as_markup(resize_keyboard=True)

    
    @staticmethod
    def confirmation(lang: str) -> ReplyKeyboardMarkup:
        """Confirm/Refill/Cancel"""
        builder = ReplyKeyboardBuilder()
        builder.row(KeyboardButton(text=btn(lang, "confirm")))
        builder.row(
            KeyboardButton(text=btn(lang, "refill")),
            KeyboardButton(text=btn(lang, "cancel"))
        )
        return builder.as_markup(resize_keyboard=True)

    @staticmethod
    def admin_menu(lang: str) -> ReplyKeyboardMarkup:
        """Admin panel menu"""
        builder = ReplyKeyboardBuilder()
        builder.row(KeyboardButton(text="📊 Statistics"))
        builder.row(KeyboardButton(text="⏳ Pending Applications"))
        builder.row(KeyboardButton(text=btn(lang, "back")))
        return builder.as_markup(resize_keyboard=True)