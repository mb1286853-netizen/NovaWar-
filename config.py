import os

BOT_TOKEN = os.getenv('BOT_TOKEN')
ADMIN_IDS = list(map(int, os.getenv('ADMIN_IDS', '123456789').split(',')))

# محافظت از کاربران خاص
PROTECTED_USERS = ADMIN_IDS + [777000]  # مالک + ربات تلگرام

# تنظیمات بازی
INITIAL_COINS = 1000
INITIAL_GEMS = 10
INITIAL_LEVEL = 1
