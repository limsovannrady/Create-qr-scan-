import os
import asyncio
import logging
from telegram import Bot
from telegram.ext import ApplicationBuilder
from db import init_db
from bot_handlers import register_handlers

TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.WARNING
)


async def delete_webhook(token):
    bot = Bot(token=token)
    async with bot:
        await bot.delete_webhook(drop_pending_updates=True)


def main():
    if not TOKEN:
        print("ERROR: TELEGRAM_BOT_TOKEN is not set!")
        return

    init_db()

    asyncio.run(delete_webhook(TOKEN))

    app = ApplicationBuilder().token(TOKEN).build()
    register_handlers(app)

    print("Bot Running...")
    app.run_polling()


if __name__ == "__main__":
    main()
