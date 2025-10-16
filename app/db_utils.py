import asyncio
from pymongo.errors import PyMongoError
from config import user_collection, achievements_collection
from utils import logger

DEFAULT_USER_FIELDS = {
    "roses": 0,
    "peonies": 0,
    "last_used_time_rose": 0.0,
    "last_used_time_peonies": 0.0,
    "use_count_rose": 0,
    "use_count_peonies": 0,
    "nickname": "User",
    "username": "Unknown"
}

def _create_user_document(user_id: str) -> dict:
    return {"user_id": user_id, **DEFAULT_USER_FIELDS.copy()}

async def load_user_data(user_id: str) -> dict | None:
    try:
        user_data = await asyncio.to_thread(user_collection.find_one, {"user_id": user_id})
        if not user_data:
            new_user_doc = _create_user_document(user_id)
            await asyncio.to_thread(user_collection.insert_one, new_user_doc)
            logger.info(f"Created new user data for {user_id}")
            return new_user_doc
        
        updated = False
        for key, default_value in DEFAULT_USER_FIELDS.items():
            if key not in user_data:
                user_data[key] = default_value
                updated = True
        if updated:
            await save_user_data(user_data)
            logger.info(f"Updated user_data for {user_id} with default fields.")
        return user_data
    except PyMongoError as e:
        logger.error(f"PyMongoError loading/creating user data for {user_id}: {e}")
    except Exception as e:
        logger.error(f"Unexpected error loading/creating user data for {user_id}: {e}")
    return None

async def save_user_data(user_data: dict) -> bool:
    if "user_id" not in user_data:
        logger.error("Attempted to save user_data without user_id")
        return False
    try:
        await asyncio.to_thread(
            user_collection.update_one,
            {"user_id": user_data["user_id"]},
            {"$set": user_data},
            upsert=True
        )
        return True
    except PyMongoError as e:
        logger.error(f"PyMongoError saving user data for {user_data['user_id']}: {e}")
    except Exception as e:
        logger.error(f"Unexpected error saving user data for {user_data['user_id']}: {e}")
    return False

async def load_all_users() -> list:
    try:
        users_cursor = await asyncio.to_thread(user_collection.find)
        return list(users_cursor)
    except PyMongoError as e:
        logger.error(f"PyMongoError loading all users: {e}")
    except Exception as e:
        logger.error(f"Unexpected error loading all users: {e}")
    return []

async def load_achievements(user_id: str) -> list:
    try:
        achievements_doc = await asyncio.to_thread(achievements_collection.find_one, {"user_id": user_id})
        if not achievements_doc:
            new_achievements_doc = {"user_id": user_id, "achievements": []}
            await asyncio.to_thread(achievements_collection.insert_one, new_achievements_doc)
            logger.info(f"Created new achievements data for {user_id}")
            return []
        return achievements_doc.get("achievements", [])
    except PyMongoError as e:
        logger.error(f"PyMongoError loading/creating achievements for {user_id}: {e}")
    except Exception as e:
        logger.error(f"Unexpected error loading/creating achievements for {user_id}: {e}")
    return []

async def save_achievements(user_id: str, achievements: list) -> bool:
    try:
        await asyncio.to_thread(
            achievements_collection.update_one,
            {"user_id": user_id},
            {"$set": {"achievements": achievements}},
            upsert=True
        )
        return True
    except PyMongoError as e:
        logger.error(f"PyMongoError saving achievements for {user_id}: {e}")
    except Exception as e:
        logger.error(f"Unexpected error saving achievements for {user_id}: {e}")
    return False

def init_db_indexes():
    try:
        user_collection.create_index([("user_id", 1)], unique=True, background=True)
        achievements_collection.create_index([("user_id", 1)], unique=True, background=True)
        logger.info("Database indexes check/creation initiated.")
    except PyMongoError as e:
        logger.error(f"PyMongoError creating DB indexes: {e}")
    except Exception as e:
        logger.error(f"Unexpected error creating DB indexes: {e}")