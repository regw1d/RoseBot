from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from app.game_mechanics import process_item_collection
from app.text_utils import get_rose_word_form

rose_router = Router()

@rose_router.message(Command("rose"))
async def handle_rose_command(message: Message):
    await process_item_collection(message, "rose", get_rose_word_form)