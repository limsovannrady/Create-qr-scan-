import os
import time
import json
import logging
import urllib.request
from telegram.ext import ApplicationBuilder
from db import init_db
from bot_handlers import register_handlers

TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.WARNING
)


def delete_webhook_sync(token):
    url = f"https://api.telegram.org/bot{token}/deleteWebhook"
    try:
        payload = json.dumps({"drop_pending_updates": True}).encode("utf-8")
        req = urllib.request.Request(url, data=payload,
                                     headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read())
        if data.get("ok"):
            print("Webhook deleted successfully.")
        else:
            print(f"deleteWebhook response: {data}")
    except Exception as e:
        print(f"Warning: could not delete webhook: {e}")


def main():
    if not TOKEN:
        print("ERROR: TELEGRAM_BOT_TOKEN is not set!")
        return

    init_db()

    print("Deleting any active webhook...")
    delete_webhook_sync(TOKEN)
    time.sleep(3)

    app = ApplicationBuilder().token(TOKEN).build()
    register_handlers(app)

    print("Bot Running...")
    app.run_polling(drop_pending_updates=True)


if __name__ == "__main__":
    main()
