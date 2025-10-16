import asyncio
from aiogram import Bot, Dispatcher
from config import TOKEN
from app.handlers import router as main_router
from app.rose import rose_router
from app.peonies import peonies_router
from app.db_utils import init_db_indexes
from utils import logger

async def main():
    if not TOKEN:
        logger.critical("TOKEN is not set in config.py or .env file. Bot cannot start.")
        return

    bot = Bot(token=TOKEN)
    dp = Dispatcher()

    init_db_indexes()

    dp.include_router(main_router)
    dp.include_router(rose_router)
    dp.include_router(peonies_router)

    await bot.delete_webhook(drop_pending_updates=True)
    logger.info("Webhook deleted, starting polling...")

    try:
        logger.info('= - = - = - = - = - Bot has been started! = - = - = - = - = -')
        await dp.start_polling(bot)
    except KeyboardInterrupt:
        logger.info("Bot stopped by user (KeyboardInterrupt).")
    except Exception as e:
        logger.error(f"An error occurred during bot polling: {e}", exc_info=True)
    finally:
        logger.info("Shutting down bot...")
        await bot.session.close()
        logger.info("= - = - = - = - = - Bot has been stopped! = - = - = - = - = -")


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except RuntimeError as e:
        logger.error(f"RuntimeError running main: {e}")
    except Exception as e:
        logger.critical(f"Critical error during script execution: {e}", exc_info=True)

# python 3.13.0 | aiogram 3.22.0 | last format day 16.10.2025 - 14:23 | RoseBot - @regwid_RoseBot ~