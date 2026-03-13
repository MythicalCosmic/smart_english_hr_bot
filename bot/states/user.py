"""
FSM states
"""
from aiogram.fsm.state import State, StatesGroup

class MenuState(StatesGroup):
    main = State()
    settings = State()
    language_select = State()


class AdminState(StatesGroup):
    main = State()
    viewing_app = State()
    adding_note = State()


class ApplicationState(StatesGroup):
    first_name = State()
    last_name = State()
    birth_date = State()
    gender = State()
    address = State()
    phone = State()
    email = State()
    is_student = State()
    education_place = State()
    education_level = State()
    additional_courses = State()
    additional_courses_subject = State()
    marriage_status = State()
    if_children = State()
    russian_level = State()
    russian_voice = State()
    english_level = State()
    english_voice = State()
    has_experience = State()
    experience_years = State()
    last_workplace = State()
    last_position = State()
    photo = State()
    resume = State()
    how_found = State()
    additional_notes = State()
    confirmation = State()
