from aiogram import Router, F, Bot
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from aiogram.exceptions import TelegramBadRequest

from app.keyboards import donate_keyboard, stats_keyboard
from app.db_utils import load_all_users as db_load_all_users
from app.db_utils import load_achievements as db_load_achievements
from app.text_utils import get_rose_word_form, get_peonies_word_form
from app.game_mechanics import process_item_collection

from config import RULES, CHANNEL, ALL_ACHIEVEMENTS_LIST, PAGE_SIZE
from utils import logger

import random

router = Router()

hot_rose = ['роза','розы','роз']
hot_stats = ['статы','статс','стат']
hot_achie = ['ачивки','ачи','достяги']
hot_peonies = ['пион','пионы','пиона']

@router.message(CommandStart())
async def start(message: Message):
    user_first_name = message.from_user.first_name if message.from_user else "Гость"
    await message.reply(
        f'Привет {user_first_name}! 🌹\n\n'
        'Это первый полу-законченый проект от @regwid1337 связанный с ТГ ботом и... Цветами.\nДля подробной информации пропиши команды /help или /rules'
    )

@router.message(Command("help"))
async def help(message: Message):
    await message.reply(
        'Доступные команды бота:\n'
        '🟦 /start – Стартовая команда бота.\n'
        '🟦 /help – Справка.\n'
        '🟦 /rose – Фарм роз.\n'
        '🟦 /peonies – Фарм пионов.\n'
        '🟦 /hotwords – Список хот-вордов бота.\n'
        '🟦 /donate – Поддержать разработчика.\n'
        '🟦 /stats – Статистика (с листами).\n'
        '🟦 /fstats – Полная статистика (только в ЛС).\n'
        '🟦 /achie – Достижения.\n'
        '🟦 /rules – Правила использования.\n'
        '🟦 /helpersdev – Авторы бота.\n'
        '🟦 /regchan – Присоединиться к каналу новостей.\n'
        '🟦 /seasons – Ежемесечные сезоны.\n'
        '🛠 Для корректной работы с "горячими словами" (хот-вордов) дай мне права администратора.'
    )

@router.message(Command("hotwords"))
async def hotwords(message: Message):
    await message.reply(
        'Хот-ворды бота:\n'
        f'{", ".join(hot_rose)} - Фарм роз\n'
        f'{", ".join(hot_peonies)} - Фарм пионов\n'
        f'{", ".join(hot_stats)} - Статистика\n'
        f'{", ".join(hot_achie)} - Достижения\n'
    )

async def _check_admin_for_hotwords(message: Message) -> bool:
    try:
        bot_member = await message.bot.get_chat_member(message.chat.id, message.bot.id)
        if bot_member.status != "administrator":
            await message.reply("Для работы с хот-вордами мне нужны права администратора!")
            return False
        return True
    except Exception as e:
        logger.error(f"Error checking bot admin status in hotword: {e}")
        await message.reply("Произошла ошибка при проверке прав. Попробуйте позже.")
        return False

@router.message(
    F.text,
    lambda msg: not msg.text.startswith('/'),
    lambda msg: any(word in msg.text.lower().split() for word in hot_rose)
)
async def handle_hotwords_rose_wrapper(message: Message):
    if await _check_admin_for_hotwords(message):
        await process_item_collection(message, "rose", get_rose_word_form)

@router.message(
    F.text,
    lambda msg: not msg.text.startswith('/'),
    lambda msg: any(word in msg.text.lower().split() for word in hot_peonies)
)
async def handle_hotwords_peonies_wrapper(message: Message):
    if await _check_admin_for_hotwords(message):
        await process_item_collection(message, "peony", get_peonies_word_form)

@router.message(
    F.text,
    lambda msg: not msg.text.startswith('/'),
    lambda msg: any(word in msg.text.lower().split() for word in hot_stats)
)
async def handle_hot_stats(message: Message):
    await handle_stats_command(message, is_hotword=True)

@router.message(
    F.text,
    lambda msg: not msg.text.startswith('/'),
    lambda msg: any(word in msg.text.lower().split() for word in hot_achie)
)
async def handle_hot_achie(message: Message):
    await show_achievements(message)

@router.message(Command("donate"))
async def donate(message: Message):
    markup = donate_keyboard()
    await message.reply("Поддержать автора можно тут:", reply_markup=markup)
    
@router.message(Command("stats"))
async def handle_stats_command(message: Message, is_hotword: bool = False):
    editable_message_id = message.message_id if not is_hotword else None
    await show_page_stats(message.bot, message.chat.id, editable_message_id, page=0, reply_to_message_id=message.message_id if is_hotword else None)

async def show_page_stats(bot: Bot, chat_id: int, message_id_to_edit: int | None, page: int, reply_to_message_id: int | None = None):
    data = await db_load_all_users()
    if not data:
        text_no_data = 'Пока никто не собирал цветы.☹️'
        if message_id_to_edit:
            try:
                await bot.edit_message_text(chat_id=chat_id, message_id=message_id_to_edit, text=text_no_data, reply_markup=None)
            except TelegramBadRequest:
                await bot.send_message(chat_id=chat_id, text=text_no_data, reply_to_message_id=reply_to_message_id)
        else:
            await bot.send_message(chat_id=chat_id, text=text_no_data, reply_to_message_id=reply_to_message_id)
        return

    stats = sorted(data, key=lambda x: (x.get('roses', 0) + x.get('peonies', 0)), reverse=True)
    
    total_pages = (len(stats) + PAGE_SIZE - 1) // PAGE_SIZE
    start_index = page * PAGE_SIZE
    end_index = start_index + PAGE_SIZE
    current_page_users = stats[start_index:end_index]

    if not current_page_users:
        await bot.send_message(chat_id=chat_id, text='Ошибка отображения страницы статистики.', reply_to_message_id=reply_to_message_id)
        return

    stats_message_text = "🌹🌸 Топ пользователей:\n"
    for i, user_data_doc in enumerate(current_page_users, start=start_index + 1):
        roses = user_data_doc.get('roses', 0)
        peonies = user_data_doc.get('peonies', 0)
        username_display = user_data_doc.get('username', 'Unknown')
        nickname_display = user_data_doc.get('nickname', 'User')
        stats_message_text += f"{i}. {username_display} ({nickname_display}): " \
                              f"{roses} {get_rose_word_form(roses)}, {peonies} {get_peonies_word_form(peonies)}\n"
    
    markup = stats_keyboard(page, total_pages)
    
    try:
        if message_id_to_edit:
            await bot.edit_message_text(chat_id=chat_id, message_id=message_id_to_edit, text=stats_message_text, reply_markup=markup)
        else:
            await bot.send_message(chat_id=chat_id, text=stats_message_text, reply_markup=markup, reply_to_message_id=reply_to_message_id)
    except TelegramBadRequest as e:
        logger.warning(f"Failed to edit stats message, sending new one. Error: {e}")
        await bot.send_message(chat_id=chat_id, text=stats_message_text, reply_markup=markup, reply_to_message_id=reply_to_message_id)
    except Exception as e:
        logger.error(f"Unexpected error in show_page_stats: {e}")
        await bot.send_message(chat_id=chat_id, text="Ошибка при отображении статистики.", reply_to_message_id=reply_to_message_id)


@router.callback_query(F.data.startswith("stats:"))
async def handle_stats_pagination(callback: CallbackQuery):
    if not callback.message:
        await callback.answer("Не могу обработать этот запрос.")
        return
    try:
        page_str = callback.data.split(":")[1]
        page = int(page_str)
        await show_page_stats(callback.bot, callback.message.chat.id, callback.message.message_id, page=page)
    except (ValueError, IndexError) as e:
        logger.error(f"Invalid page number or format in callback data: {callback.data}. Error: {e}")
        await callback.answer("Ошибка данных пагинации.")
    except Exception as e:
        logger.error(f"Error in handle_stats_pagination: {e}")
        await callback.answer("Произошла ошибка.")
    finally:
        await callback.answer()

@router.message(Command("fstats"))
async def show_full_statistics(message: Message):
    if message.chat.type != "private":
        await message.reply("Эту команду можно использовать только в личных сообщениях с ботом!")
        return

    data = await db_load_all_users()
    if not data:
        await message.reply('Пока никто не собирал цветы :(')
        return
    
    stats = sorted(data, key=lambda x: (x.get('roses', 0) + x.get('peonies', 0)), reverse=True)
    
    stats_message_text = "🌹🌸 Полная статистика пользователей:\n"
    for i, user_data_doc in enumerate(stats, start=1):
        roses = user_data_doc.get('roses', 0)
        peonies = user_data_doc.get('peonies', 0)
        username_display = user_data_doc.get('username', 'Unknown')
        nickname_display = user_data_doc.get('nickname', 'User')
        stats_message_text += f"{i}. @{username_display} ({nickname_display}): " \
                              f"{roses} {get_rose_word_form(roses)}, {peonies} {get_peonies_word_form(peonies)}\n"
    
    MAX_MESSAGE_LENGTH = 4096
    if len(stats_message_text) > MAX_MESSAGE_LENGTH:
        for i in range(0, len(stats_message_text), MAX_MESSAGE_LENGTH):
            await message.reply(stats_message_text[i:i + MAX_MESSAGE_LENGTH])
    else:
        await message.reply(stats_message_text)

@router.message(Command("achie"))
async def show_achievements(message: Message):
    if not message.from_user:
        await message.reply("Не могу определить пользователя.")
        return
        
    user_id = str(message.from_user.id)
    user_achievements = await db_load_achievements(user_id)
    
    if not user_achievements:
        await message.reply("У вас пока нет достижений.")
        return

    response_text = "Ваши достижения:\n\n"
    for achie_name in user_achievements:
        detail = next((d for d in ALL_ACHIEVEMENTS_LIST if d["name"] == achie_name), None)
        if detail:
            response_text += f"🌟 *{detail['name']}*\n📖 {detail['description']}\n\n"
        else:
            response_text += f"🌟 *{achie_name}* (Описание не найдено)\n\n"
            
    try:
        await message.reply(response_text, parse_mode="Markdown")
    except TelegramBadRequest as e:
        logger.error(f"Error sending achievements with Markdown: {e}. Sending as plain text.")
        await message.reply(response_text)


@router.message(Command("rules"))
async def rules(message: Message):
    await message.reply(f'Правила бота ⬇️:\n{RULES}')

@router.message(Command("seasons"))
async def seasons(message: Message):
    await message.reply('Еще не было сезонов!')

@router.message(Command("helpersdev"))
async def helpersdev(message: Message):
    await message.reply(
        '💵 Boosty:\n'
        'xenonity - 43 руб\n'
        'Aizava - 30 руб\n'
        '💰 DonationAlerts:\n'
        'De4thlxrd - 26 руб\n'
        '🧑‍💻 Helpdev:\n'
        'Eselty, MaDeInCCCP'
    )

@router.message(Command("regchan"))
async def regchan(message: Message):
    await message.reply(f'🌹Ссылка на канал разработчика:\n{CHANNEL}')