import os
import sys
import json
import asyncio
import logging
from http.server import BaseHTTPRequestHandler

# Allow imports from project root
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from telegram import Update
from telegram.ext import ApplicationBuilder
from db import init_db
from bot_handlers import register_handlers

TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)


async def process_update(update_data: dict):
    init_db()
    app = ApplicationBuilder().token(TOKEN).build()
    register_handlers(app)
    async with app:
        update = Update.de_json(update_data, app.bot)
        await app.process_update(update)


class handler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        pass

    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"QR Bot webhook is active.")

    def do_POST(self):
        try:
            length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(length)
            update_data = json.loads(body)
            asyncio.run(process_update(update_data))
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"ok")
        except Exception as e:
            logging.error(f"Webhook error: {e}")
            self.send_response(500)
            self.end_headers()
            self.wfile.write(b"error")
