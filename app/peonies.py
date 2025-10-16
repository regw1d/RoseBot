from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from app.game_mechanics import process_item_collection
from app.text_utils import get_peonies_word_form

peonies_router = Router()

@peonies_router.message(Command("peonies"))
async def handle_peonies_command(message: Message):
    await process_item_collection(message, "peony", get_peonies_word_form)