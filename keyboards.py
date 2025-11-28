from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def main_menu():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton("پروفایل 👤", callback_data="profile")],
        [InlineKeyboardButton("حمله 💣", callback_data="attack_menu")],
        [InlineKeyboardButton("فروشگاه 🛒", callback_data="shop")],
        [InlineKeyboardButton("جعبه شانس 🎁", callback_data="boxes")],
        [InlineKeyboardButton("ماینر ⛏️", callback_data="miner")],
        [InlineKeyboardButton("پدافند 🛡️", callback_data="defense")],
        [InlineKeyboardButton("پشتیبانی 📞", callback_data="support")],
    ])

def back_kb(to="main_menu"):
    return InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton("↩️ بازگشت", callback_data=to)]])
