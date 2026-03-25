"""
Inline keyboards
"""
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_admin_list_keyboard(app_id: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="👁 Ko'rish", callback_data=f"admin_view_{app_id}")],
        [
            InlineKeyboardButton(text="✅ Qabul", callback_data=f"admin_accept_{app_id}"),
            InlineKeyboardButton(text="❌ Rad", callback_data=f"admin_reject_{app_id}")
        ]
    ])


def get_admin_app_keyboard(app_id: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="✅ Qabul qilish", callback_data=f"admin_accept_{app_id}"),
            InlineKeyboardButton(text="❌ Rad etish", callback_data=f"admin_reject_{app_id}")
        ],
        [
            InlineKeyboardButton(text="📝 Izoh qo'shish", callback_data=f"admin_note_{app_id}")
        ]
    ])
