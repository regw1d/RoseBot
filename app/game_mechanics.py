import random
from aiogram import Bot
from aiogram.types import Message
from typing import Callable

from config import ITEM_CONFIG, ACHIEVEMENTS_DEFINITIONS
from utils import logger, get_current_time_ts, format_remaining_time
from app.db_utils import load_user_data, save_user_data, load_achievements, save_achievements

def _can_use_item(last_used_time_ts: float, delay_seconds: int) -> tuple[bool, float]:
    if last_used_time_ts == 0.0:
        return True, 0.0
    elapsed_time_seconds = get_current_time_ts() - last_used_time_ts
    if elapsed_time_seconds >= delay_seconds:
        return True, 0.0
    return False, delay_seconds - elapsed_time_seconds

async def _grant_new_achievements_message(bot: Bot, chat_id: int, new_achievements: list):
    for achie_name in new_achievements:
        full_achiev_info = next(
            (ach_def for ach_type_list in ACHIEVEMENTS_DEFINITIONS.values()
             for ach_def in ach_type_list if ach_def["name"] == achie_name),
            None
        )
        description = full_achiev_info["description"] if full_achiev_info else "Описание не найдено."
        try:
            await bot.send_message(chat_id, f"Поздравляем! ⭐\nВы получили достижение:\n*{achie_name}*\n_{description}_", parse_mode="Markdown")
        except Exception as e:
            logger.error(f"Error sending achievement notification for {achie_name}: {e}")

async def _check_and_update_achievements(user_id: str, user_data: dict, item_type: str, bot_instance: Bot, chat_id: int):
    item_conf = ITEM_CONFIG[item_type]
    current_achievements_list = await load_achievements(user_id)
    if current_achievements_list is None:
        return

    newly_achieved_names = []

    usage_achiev_type = item_conf.get("achievements_usage_type")
    if usage_achiev_type and usage_achiev_type in ACHIEVEMENTS_DEFINITIONS:
        for achie_def in ACHIEVEMENTS_DEFINITIONS[usage_achiev_type]:
            if user_data.get(item_conf["db_field_use_count"], 0) >= achie_def["count"] and \
               achie_def["name"] not in current_achievements_list:
                current_achievements_list.append(achie_def["name"])
                newly_achieved_names.append(achie_def["name"])

    collection_achiev_type = item_conf.get("achievements_collection_type")
    if collection_achiev_type and collection_achiev_type in ACHIEVEMENTS_DEFINITIONS:
        for achie_def in ACHIEVEMENTS_DEFINITIONS[collection_achiev_type]:
            if user_data.get(item_conf["db_field_count"], 0) >= achie_def["count"] and \
               achie_def["name"] not in current_achievements_list:
                current_achievements_list.append(achie_def["name"])
                newly_achieved_names.append(achie_def["name"])
    
    if newly_achieved_names:
        if await save_achievements(user_id, current_achievements_list):
            await _grant_new_achievements_message(bot_instance, chat_id, newly_achieved_names)
        else:
            logger.error(f"Failed to save new achievements for user {user_id}")


async def process_item_collection(message: Message, item_type: str, word_form_func: Callable[[int], str]):
    if message.chat.type not in ["group", "supergroup"]:
        await message.reply("Эта команда работает только в группах, где я есть.")
        return

    if not message.from_user:
        await message.reply("Не удалось определить пользователя.")
        return
        
    user_id = str(message.from_user.id)
    telegram_user = message.from_user
    
    user_data = await load_user_data(user_id)
    if user_data is None:
        await message.reply("Не удалось загрузить ваши данные. Попробуйте еще раз.")
        return

    item_conf = ITEM_CONFIG[item_type]
    
    needs_save_for_user_info = False
    new_username = telegram_user.username or "Unknown"
    new_nickname = telegram_user.first_name or "User"
    if user_data.get("username") != new_username:
        user_data["username"] = new_username
        needs_save_for_user_info = True
    if user_data.get("nickname") != new_nickname:
        user_data["nickname"] = new_nickname
        needs_save_for_user_info = True
    
    last_used_ts = user_data.get(item_conf["db_field_last_used"], 0.0)
    can_use, remaining_sec = _can_use_item(last_used_ts, item_conf["delay"])
    current_item_count = user_data.get(item_conf["db_field_count"], 0)

    if not can_use:
        await message.reply(
            f"Ты уже собирал(а) {item_conf['name_plural_genitive']}.\n"
            f"Попробуй через ~ {format_remaining_time(remaining_sec)}\n"
            f"У тебя {current_item_count} {word_form_func(current_item_count)}."
        )
        if needs_save_for_user_info :
            await save_user_data(user_data)
        return

    new_items = random.randint(item_conf["min_change"], item_conf["max_change"])
    
    user_data[item_conf["db_field_count"]] = current_item_count + new_items
    user_data[item_conf["db_field_last_used"]] = get_current_time_ts()
    user_data[item_conf["db_field_use_count"]] = user_data.get(item_conf["db_field_use_count"], 0) + 1
    
    if not await save_user_data(user_data):
        await message.reply("Произошла ошибка при сохранении ваших данных. Попробуйте еще раз.")
        user_data[item_conf["db_field_count"]] -= new_items
        user_data[item_conf["db_field_last_used"]] = last_used_ts
        user_data[item_conf["db_field_use_count"]] -= 1
        return

    new_total_items = user_data[item_conf["db_field_count"]]
    
    await message.reply(
        f"{item_conf['emoji']} Вы получили {new_items} {word_form_func(new_items)}!\n"
        f"Теперь у вас {new_total_items} {word_form_func(new_total_items)}."
    )
    logger.info(f"User {user_id} ({user_data.get('nickname', 'User')}) collected {new_items} {item_type}(s). Total: {new_total_items}")

    await _check_and_update_achievements(user_id, user_data, item_type, message.bot, message.chat.id)