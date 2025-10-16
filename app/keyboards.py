from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import BOOSTY, DONATE

def donate_keyboard():
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Бустик!", url=BOOSTY)],
        [InlineKeyboardButton(text="Донат Алертс!", url=DONATE)]
    ])
    return markup

def stats_keyboard(page: int, total_pages: int):
    buttons = []
    row = []
    if page > 0:
        row.append(InlineKeyboardButton(text="⬅️ Назад", callback_data=f"stats:{page - 1}"))
    if page < total_pages - 1:
        row.append(InlineKeyboardButton(text="➡️ Вперед", callback_data=f"stats:{page + 1}"))
    
    if row:
        buttons.append(row)
        
    return InlineKeyboardMarkup(inline_keyboard=buttons)