"""
Inline keyboards
"""
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_admin_list_keyboard(app_id: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="👁 View", callback_data=f"admin_view_{app_id}")]
    ])


def get_admin_app_keyboard(app_id: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="✅ Accept", callback_data=f"admin_accept_{app_id}"),
            InlineKeyboardButton(text="❌ Reject", callback_data=f"admin_reject_{app_id}")
        ],
        [
            InlineKeyboardButton(text="📝 Add Note", callback_data=f"admin_note_{app_id}")
        ]
    ])
