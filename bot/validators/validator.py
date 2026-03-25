# bot/validators/validator.py
import re
from datetime import date
from typing import Tuple, Optional
from services.language_service import btn

class Validators:
    PHONE_PATTERN = re.compile(r"^\+?998[0-9]{9}$")
    EMAIL_PATTERN = re.compile(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")
    DATE_PATTERN = re.compile(r"^(\d{1,2})[./](\d{1,2})[./](\d{4})$")
    
    @staticmethod
    def name(text: str, min_len: int = 2, max_len: int = 50) -> Tuple[bool, str]:
        text = text.strip()
        if min_len <= len(text) <= max_len:
            return True, text
        return False, text
    
    @staticmethod
    def address(text: str) -> Tuple[bool, str]:
        text = text.strip()
        if 5 <= len(text) <= 255:
            return True, text
        return False, text
    
    @staticmethod
    def phone(text: str) -> Tuple[bool, str]:
        cleaned = re.sub(r"[\s\-\(\)]", "", text)
        if not cleaned.startswith("+"):
            cleaned = "+" + cleaned
        if Validators.PHONE_PATTERN.match(cleaned.replace("+", "")):
            return True, cleaned
        return False, text
    
    @staticmethod
    def email(text: str) -> Tuple[bool, str]:
        text = text.strip().lower()
        if Validators.EMAIL_PATTERN.match(text):
            return True, text
        return False, text
    
    @staticmethod
    def birth_date(text: str) -> Tuple[bool, Optional[date]]:
        match = Validators.DATE_PATTERN.match(text.strip())
        if not match:
            return False, None
        try:
            day, month, year = int(match.group(1)), int(match.group(2)), int(match.group(3))
            birth = date(year, month, day)
            today = date.today()
            age = today.year - birth.year - ((today.month, today.day) < (birth.month, birth.day))
            if 16 <= age <= 70:
                return True, birth
            return False, None
        except:
            return False, None
    
    @staticmethod
    def text_field(text: str, min_len: int = 2, max_len: int = 255) -> Tuple[bool, str]:
        text = text.strip()
        if min_len <= len(text) <= max_len:
            return True, text
        return False, text
    
    @staticmethod
    def experience_years(text: str) -> Tuple[bool, int]:
        try:
            years = int(text.strip())
            if 0 <= years <= 25:
                return True, years
            return False, 0
        except:
            return False, 0


# Dynamic button matchers - pulls directly from YAML
def _get_buttons(key: str) -> list:
    """Get button text for all languages from YAML"""
    return [btn("uz", key), btn("ru", key), btn("en", key)]


def is_back(text: str) -> bool:
    return text in _get_buttons("back")


def is_skip(text: str) -> bool:
    return text in _get_buttons("skip")


def is_yes(text: str) -> bool:
    return text in _get_buttons("yes")


def is_no(text: str) -> bool:
    return text in _get_buttons("no")


def is_confirm(text: str) -> bool:
    return text in _get_buttons("confirm")


def is_refill(text: str) -> bool:
    return text in _get_buttons("refill")


def is_cancel(text: str) -> bool:
    return text in _get_buttons("cancel")


def get_gender(text: str) -> Optional[str]:
    gender_map = {
        btn("uz", "male"): "male", btn("ru", "male"): "male", btn("en", "male"): "male",
        btn("uz", "female"): "female", btn("ru", "female"): "female", btn("en", "female"): "female",
    }
    return gender_map.get(text)


def get_level(text: str) -> Optional[str]:
    """Get education level for Uzbekistan system"""
    level_map = {
        # O'rta (Secondary)
        btn("uz", "secondary"): "secondary",
        btn("ru", "secondary"): "secondary", 
        btn("en", "secondary"): "secondary",
        
        # O'rta maxsus (Specialized secondary - college/vocational)
        btn("uz", "specialized_secondary"): "specialized_secondary",
        btn("ru", "specialized_secondary"): "specialized_secondary",
        btn("en", "specialized_secondary"): "specialized_secondary",
        
        # Oliy to'liqsiz (Incomplete higher - bachelor in progress)
        btn("uz", "incomplete_higher"): "incomplete_higher",
        btn("ru", "incomplete_higher"): "incomplete_higher",
        btn("en", "incomplete_higher"): "incomplete_higher",
        
        # Oliy (Higher - bachelor's degree)
        btn("uz", "bachelor"): "bachelor",
        btn("ru", "bachelor"): "bachelor",
        btn("en", "bachelor"): "bachelor",
        
        # Magistratura (Master's)
        btn("uz", "master"): "master",
        btn("ru", "master"): "master",
        btn("en", "master"): "master",
    }
    return level_map.get(text)


def get_english_level(text: str) -> Optional[str]:
    """Get English proficiency level from button text"""
    level_map = {
        btn("uz", "eng_past"): "past",
        btn("ru", "eng_past"): "past",
        btn("en", "eng_past"): "past",
        btn("uz", "eng_ortacha"): "ortacha",
        btn("ru", "eng_ortacha"): "ortacha",
        btn("en", "eng_ortacha"): "ortacha",
        btn("uz", "eng_ilgor"): "ilgor",
        btn("ru", "eng_ilgor"): "ilgor",
        btn("en", "eng_ilgor"): "ilgor",
    }
    return level_map.get(text)


def get_selected_lang(text: str) -> Optional[str]:
    """Get language code from button text"""
    lang_map = {
        btn("uz", "uz"): "uz",
        btn("ru", "ru"): "ru",
        btn("en", "en"): "en",
    }
    return lang_map.get(text)