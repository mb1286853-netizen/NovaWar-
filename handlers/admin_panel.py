from aiogram import types, F
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import sqlite3

# توابع پنل ادمین اینجا میاد
# فعلاً خالی می‌ذاریم، بعداً کامل می‌کنیم

def create_admin_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="👥 کاربران", callback_data="admin_users")],
        [InlineKeyboardButton(text="📊 آمار", callback_data="admin_stats")],
        [InlineKeyboardButton(text="🔙 بازگشت", callback_data="admin_back")]
    ])  # ✅ اینجا پرانتز بسته شد
