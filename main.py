import os
import logging
import sqlite3
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import BOT_TOKEN, ADMIN_IDS, PROTECTED_USERS

# تنظیمات لاگ
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

if not BOT_TOKEN:
    logger.error("❌ BOT_TOKEN تنظیم نشده!")
    exit(1)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# بررسی ادمین
def is_admin(user_id: int) -> bool:
    return user_id in ADMIN_IDS

# بررسی کاربر محافظت شده
def is_protected(user_id: int) -> bool:
    return user_id in PROTECTED_USERS

# دیتابیس
def init_db():
    conn = sqlite3.connect('zone.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            username TEXT,
            zone_coin INTEGER DEFAULT 1000,
            zone_gem INTEGER DEFAULT 10,
            xp INTEGER DEFAULT 0,
            level INTEGER DEFAULT 1,
            power INTEGER DEFAULT 100,
            defense_level INTEGER DEFAULT 1,
            cyber_level INTEGER DEFAULT 1,
            missiles TEXT DEFAULT '[]',
            drones TEXT DEFAULT '[]',
            language TEXT DEFAULT 'fa',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# ==================== دستورات کاربران ====================

@dp.message(Command("start"))
async def start_command(message: types.Message):
    user_id = message.from_user.id
    username = message.from_user.username or "ناشناس"
    
    conn = sqlite3.connect('zone.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT OR IGNORE INTO users (user_id, username) 
        VALUES (?, ?)
    ''', (user_id, username))
    conn.commit()
    conn.close()
    
    await message.answer(
        "🚀 **به ربات WarZone خوش آمدید!**\n\n"
        "⚔️ یک ربات جنگی پیشرفته\n\n"
        "🔸 /profile - پروفایل شما\n"
        "🔸 /attack - حمله به دشمن\n"
        "🔸 /shop - فروشگاه\n"
        "🔸 /premium_shop - فروشگاه ویژه\n"
        "🔸 /league - لیگ‌ها\n\n"
        "🛡 کاربران محافظت شده: مالک و ربات‌ها\n"
        "❌ به این کاربران نمی‌توان حمله کرد!"
    )

@dp.message(Command("profile"))
async def profile_command(message: types.Message):
    user_id = message.from_user.id
    
    conn = sqlite3.connect('zone.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
    user = cursor.fetchone()
    conn.close()
    
    if user:
        protected_status = "✅ بله" if is_protected(user_id) else "❌ خیر"
        await message.answer(
            f"👤 **پروفایل شما:**\n"
            f"💎 سکه: {user[2]:,}\n"
            f"💠 جم: {user[3]}\n"
            f"⭐ XP: {user[4]:,}\n"
            f"🆙 سطح: {user[5]}\n"
            f"💪 قدرت: {user[6]:,}\n"
            f"🛡 دفاع: سطح {user[7]}\n"
            f"🔒 امنیت سایبری: سطح {user[8]}\n"
            f"🛡 محافظت شده: {protected_status}\n"
            f"🌐 زبان: {user[10]}"
        )

@dp.message(Command("attack"))
async def attack_command(message: types.Message):
    # سیستم حمله ساده شده
    if message.reply_to_message:
        target_user = message.reply_to_message.from_user
        
        # بررسی محافظت شده بودن هدف
        if is_protected(target_user.id):
            await message.answer("❌ **خطا:** به این کاربر نمی‌توان حمله کرد! (محافظت شده)")
            return
        
        # حمله موفق
        await message.answer(
            f"⚔️ **حمله موفق!**\n\n"
            f"🎯 هدف: {target_user.first_name}\n"
            f"💥 خسارت: 1,200\n"
            f"💰 غنیمت: 150 سکه\n"
            f"⭐ XP کسب شده: 50\n\n"
            f"🛡 کاربران محافظت شده قابل حمله نیستند!"
        )
    else:
        await message.answer(
            "⚔️ **سیستم حمله**\n\n"
            "برای حمله، روی پیام کاربر مورد نظر ریپلای کن و دستور /attack رو بفرست!\n\n"
            "❌ **نکته:** به مالک ربات و ربات‌های دیگر نمی‌توان حمله کرد!"
        )

# ==================== پنل ادمین ====================

@dp.message(Command("admin"))
async def admin_command(message: types.Message):
    if not is_admin(message.from_user.id):
        await message.answer("❌ دسترسی denied!")
        return
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="👥 مدیریت کاربران", callback_data="admin_users")],
        [InlineKeyboardButton(text="📊 آمار ربات", callback_data="admin_stats")],
        [InlineKeyboardButton(text="🎁 giveaway", callback_data="admin_giveaway")],
        [InlineKeyboardButton(text="📢 ارسال پیام همگانی", callback_data="admin_broadcast")]
    ])
    
    await message.answer(
        "🛠 **پنل مدیریت WarZone**\n\n"
        "به پنل ادمین خوش آمدید!\n\n"
        f"👑 ادمین‌ها: {len(ADMIN_IDS)} کاربر\n"
        f"🛡 کاربران محافظت شده: {len(PROTECTED_USERS)} کاربر",
        reply_markup=keyboard
    )

# مدیریت کاربران
@dp.callback_query(F.data == "admin_users")
async def admin_users_menu(callback: types.CallbackQuery):
    if not is_admin(callback.from_user.id):
        return
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔍 جستجوی کاربر", callback_data="admin_search_user")],
        [InlineKeyboardButton(text="📝 ویرایش کاربر", callback_data="admin_edit_user")],
        [InlineKeyboardButton(text="🔙 بازگشت", callback_data="admin_back")]
    ])
    
    await callback.message.edit_text(
        "👥 **مدیریت کاربران**\n\n"
        "گزینه مورد نظر را انتخاب کنید:",
        reply_markup=keyboard
    )

# آمار ربات
@dp.callback_query(F.data == "admin_stats")
async def admin_stats(callback: types.CallbackQuery):
    if not is_admin(callback.from_user.id):
        return
    
    conn = sqlite3.connect('zone.db')
    cursor = conn.cursor()
    
    cursor.execute('SELECT COUNT(*) FROM users')
    total_users = cursor.fetchone()[0]
    
    cursor.execute('SELECT COUNT(*) FROM users WHERE xp > 0')
    active_users = cursor.fetchone()[0]
    
    cursor.execute('SELECT SUM(zone_coin) FROM users')
    total_coins = cursor.fetchone()[0] or 0
    
    cursor.execute('SELECT SUM(zone_gem) FROM users')
    total_gems = cursor.fetchone()[0] or 0
    
    conn.close()
    
    stats_text = (
        f"📊 **آمار ربات WarZone**\n\n"
        f"👥 کل کاربران: {total_users:,}\n"
        f"🔥 کاربران فعال: {active_users:,}\n"
        f"💰 مجموع سکه‌ها: {total_coins:,}\n"
        f"💎 مجموع جم‌ها: {total_gems}\n"
        f"👑 ادمین‌ها: {len(ADMIN_IDS)}\n"
        f"🛡 کاربران محافظت شده: {len(PROTECTED_USERS)}"
    )
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔄 بروزرسانی", callback_data="admin_stats")],
        [InlineKeyboardButton(text="🔙 بازگشت", callback_data="admin_back")]
    ])
    
    await callback.message.edit_text(stats_text, reply_markup=keyboard)

# بازگشت به منوی اصلی
@dp.callback_query(F.data == "admin_back")
async def admin_back(callback: types.CallbackQuery):
    if not is_admin(callback.from_user.id):
        return
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="👥 مدیریت کاربران", callback_data="admin_users")],
        [InlineKeyboardButton(text="📊 آمار ربات", callback_data="admin_stats")],
        [InlineKeyboardButton(text="🎁 giveaway", callback_data="admin_giveaway")],
        [InlineKeyboardButton(text="📢 ارسال پیام همگانی", callback_data="admin_broadcast")]
    ])
    
    await callback.message.edit_text(
        "🛠 **پنل مدیریت WarZone**\n\n"
        "به پنل ادمین خوش آمدید!",
        reply_markup=keyboard
    )

# ==================== دستورات سریع ادمین ====================

@dp.message(Command("addcoins"))
async def quick_add_coins(message: types.Message):
    if not is_admin(message.from_user.id):
        await message.answer("❌ دسترسی denied!")
        return
    
    try:
        args = message.text.split()
        if len(args) != 3:
            await message.answer("❌ فرمت: /addcoins user_id amount")
            return
        
        user_id, amount = int(args[1]), int(args[2])
        
        conn = sqlite3.connect('zone.db')
        cursor = conn.cursor()
        
        # بررسی وجود کاربر
        cursor.execute('SELECT zone_coin FROM users WHERE user_id = ?', (user_id,))
        if not cursor.fetchone():
            await message.answer("❌ کاربر یافت نشد!")
            return
        
        cursor.execute('UPDATE users SET zone_coin = zone_coin + ? WHERE user_id = ?', (amount, user_id))
        conn.commit()
        conn.close()
        
        await message.answer(f"✅ {amount:,} سکه به کاربر {user_id} اضافه شد!")
        
    except Exception as e:
        await message.answer(f"❌ خطا: {str(e)}")

@dp.message(Command("addgems"))
async def quick_add_gems(message: types.Message):
    if not is_admin(message.from_user.id):
        await message.answer("❌ دسترسی denied!")
        return
    
    try:
        args = message.text.split()
        if len(args) != 3:
            await message.answer("❌ فرمت: /addgems user_id amount")
            return
        
        user_id, amount = int(args[1]), int(args[2])
        
        conn = sqlite3.connect('zone.db')
        cursor = conn.cursor()
        
        cursor.execute('SELECT zone_gem FROM users WHERE user_id = ?', (user_id,))
        if not cursor.fetchone():
            await message.answer("❌ کاربر یافت نشد!")
            return
        
        cursor.execute('UPDATE users SET zone_gem = zone_gem + ? WHERE user_id = ?', (amount, user_id))
        conn.commit()
        conn.close()
        
        await message.answer(f"✅ {amount} جم به کاربر {user_id} اضافه شد!")
        
    except Exception as e:
        await message.answer(f"❌ خطا: {str(e)}")

@dp.message(Command("setlevel"))
async def quick_set_level(message: types.Message):
    if not is_admin(message.from_user.id):
        await message.answer("❌ دسترسی denied!")
        return
    
    try:
        args = message.text.split()
        if len(args) != 3:
            await message.answer("❌ فرمت: /setlevel user_id level")
            return
        
        user_id, level = int(args[1]), int(args[2])
        
        conn = sqlite3.connect('zone.db')
        cursor = conn.cursor()
        
        cursor.execute('SELECT level FROM users WHERE user_id = ?', (user_id,))
        if not cursor.fetchone():
            await message.answer("❌ کاربر یافت نشد!")
            return
        
        cursor.execute('UPDATE users SET level = ? WHERE user_id = ?', (level, user_id))
        conn.commit()
        conn.close()
        
        await message.answer(f"✅ سطح کاربر {user_id} به {level} تنظیم شد!")
        
    except Exception as e:
        await message.answer(f"❌ خطا: {str(e)}")

# ==================== فروشگاه ====================

@dp.message(Command("shop"))
async def shop_command(message: types.Message):
    await message.answer(
        "🛒 **فروشگاه WarZone**\n\n"
        
        "💣 **موشک‌ها:**\n"
        "• Tomahawk - 900 damage - 500 سکه\n"
        "• Brahmos - 1300 damage - 800 سکه\n"
        "• Iskander - 2000 damage - 1200 سکه\n\n"
        
        "🚁 **پهپادها:**\n"
        "• MQ-9 Reaper - +300 damage - 700 سکه\n"
        "• Switchblade - +500 damage - 900 سکه\n\n"
        
        "💎 برای فروشگاه ویژه: /premium_shop"
    )

@dp.message(Command("premium_shop"))
async def premium_shop_command(message: types.Message):
    await message.answer(
        "💎 **فروشگاه ویژه - فقط با جم**\n\n"
        
        "🚀 **موشک‌های ویژه:**\n"
        "• DF-41 - 7,500 damage - 15 جم\n"
        "• RS-28 Sarmat - 9,000 damage - 20 جم\n"
        "• AGM-183 ARRW - 12,000 damage - 35 جم\n"
        "• 3M22 Zircon - 13,000 damage - 40 جم\n\n"
        
        "💰 برای خرید جم: /buy_gems\n"
        "💎 وضعیت جم شما: /my_gems"
    )

async def main():
    logger.info("🤖 ربات WarZone شروع به کار کرد...")
    logger.info(f"👑 ادمین‌ها: {ADMIN_IDS}")
    logger.info(f"🛡 کاربران محافظت شده: {PROTECTED_USERS}")
    await dp.start_polling(bot)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
