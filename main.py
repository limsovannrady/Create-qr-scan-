import os
import json
import logging
import urllib.request
from http.server import HTTPServer
from db import init_db
from dashboard import handler

TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
WEBHOOK_URL = "https://create-qr-scan.vercel.app/api/webhook"

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.WARNING
)


def set_webhook(token, webhook_url):
    url = f"https://api.telegram.org/bot{token}/setWebhook"
    try:
        payload = json.dumps({"url": webhook_url, "drop_pending_updates": True}).encode("utf-8")
        req = urllib.request.Request(url, data=payload,
                                     headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read())
        if data.get("ok"):
            print(f"Webhook set successfully: {webhook_url}")
        else:
            print(f"setWebhook response: {data}")
    except Exception as e:
        print(f"Warning: could not set webhook: {e}")


def main():
    if not TOKEN:
        print("ERROR: TELEGRAM_BOT_TOKEN is not set!")
        return

    init_db()

    print("Setting webhook to Vercel...")
    set_webhook(TOKEN, WEBHOOK_URL)

    print("Dashboard running on http://0.0.0.0:5000")
    server = HTTPServer(("0.0.0.0", 5000), handler)
    server.serve_forever()


if __name__ == "__main__":
    main()
