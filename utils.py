import time
from config import CHANNEL_ID
from main import bot

async def check_membership(user_id):
    try:
        member = await bot.get_chat_member(CHANNEL_ID, user_id)
        return member.status in ["member", "administrator", "creator"]
    except:
        return False

def format_number(num):
    return f"{num:,}".replace(",", "٬")
