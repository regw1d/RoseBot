import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
if not TOKEN:
    raise ValueError("Необходимо установить переменную окружения TELEGRAM_BOT_TOKEN")

OWNER_ID = None
BOOSTY = 'https://boosty.to/regw1d'
DONATE = 'https://www.donationalerts.com/r/regw1d'
CHANNEL = None
RULES = 'https://telegra.ph/RoseBot-Rules-RUEN-11-20'

MONGO_URI = os.getenv("MONGO_URI", 'HERE set your mongo url (data base) from .env')
DB_NAME = 'RoseBotDataBase'

client = MongoClient(MONGO_URI)
db = client[DB_NAME]
user_collection = db['user_data']
achievements_collection = db['achievements']

ITEM_CONFIG = {
    "rose": {
        "name_singular": "роза",
        "name_plural_genitive": "роз",
        "delay": 7200,
        "min_change": 1,
        "max_change": 10,
        "db_field_count": "roses",
        "db_field_last_used": "last_used_time_rose",
        "db_field_use_count": "use_count_rose",
        "emoji": "🌹",
        "achievements_usage_type": "rose_usage",
        "achievements_collection_type": "rose_collection"
    },
    "peony": {
        "name_singular": "пион",
        "name_plural_genitive": "пионов",
        "delay": 14400,
        "min_change": 1,
        "max_change": 5,
        "db_field_count": "peonies",
        "db_field_last_used": "last_used_time_peonies",
        "db_field_use_count": "use_count_peonies",
        "emoji": "🌸",
        "achievements_usage_type": "peony_usage",
        "achievements_collection_type": "peony_collection"
    }
}

ACHIEVEMENTS_DEFINITIONS = {
    "rose_usage": [
        {"name": "Первые шаги!", "count": 5, "description": "5 использований команды /rose!"},
        {"name": "Любитель времени!", "count": 25, "description": "25 использований команды /rose!"},
        {"name": "В попытках постоянного...", "count": 50, "description": "50 использований команды /rose!"},
        {"name": "Потерянный во времени...", "count": 80, "description": "80 использований команды /rose!"},
        {"name": "Что такое время?", "count": 200, "description": "200 использований команды /rose!"}
    ],
    "rose_collection": [
        {"name": "Первые розы!", "count": 11, "description": "Получите 11 роз!"},
        {"name": "50 роз!", "count": 50, "description": "Соберите 50 роз!"},
        {"name": "101 роза!", "count": 101, "description": "Соберите 101 розу :)"},
        {"name": "200 роз!", "count": 200, "description": "Соберите 200 красных цветков..."},
        {"name": "500 роз!", "count": 500, "description": "Соберите 500 алых цветов..."}
    ],
    "peony_usage": [
        {"name": "Первые пионы!", "count": 5, "description": "5 использований команды /peonies!"},
        {"name": "Любитель пионов!", "count": 25, "description": "25 использований команды /peonies!"},
        {"name": "К чему эти пионы...", "count": 50, "description": "50 использований команды /peonies!"},
    ],
    "peony_collection": [
        {"name": "10 розовых цветков...", "count": 10, "description": "Соберите 10 пионов!"},
        {"name": "Пионный сад!", "count": 50, "description": "Соберите 50 пионов!"},
        {"name": "Зачем ты их собирал?", "count": 100, "description": "Соберите 100 пионов!"},
    ]
}

ALL_ACHIEVEMENTS_LIST = [
    achiev for sublist in ACHIEVEMENTS_DEFINITIONS.values() for achiev in sublist
]

PAGE_SIZE = 15