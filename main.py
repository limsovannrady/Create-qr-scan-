import os
import logging
import subprocess
import qrcode
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    last_name = update.effective_user.last_name or ""
    text = (
        f"👋 សួស្តី {last_name}\n\n"
        "ខ្ញុំជា QR Code Bot\n\n"
        "• ផ្ញើ Text / Link → បង្កើត QR Code\n"
        "• ផ្ញើរូបភាព QR → Bot នឹងស្កេនកូដ QR"
    )
    await update.message.reply_text(text, do_quote=True)


async def generate_qr(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    img = qrcode.make(text)
    file_path = "/tmp/qr.png"
    img.save(file_path)

    with open(file_path, "rb") as f:
        await update.message.reply_photo(photo=f, do_quote=True)


async def decode_qr(update: Update, context: ContextTypes.DEFAULT_TYPE):
    photo = await update.message.photo[-1].get_file()

    file_path = "/tmp/qr_input.png"
    await photo.download_to_drive(file_path)

    try:
        result = subprocess.run(
            ["zbarimg", "--raw", "-q", file_path],
            capture_output=True,
            text=True,
            timeout=10
        )
        data = result.stdout.strip()
        if data:
            await update.message.reply_text(data, do_quote=True)
        else:
            await update.message.reply_text("❌ មិនអាចអាន QR បានទេ", do_quote=True)
    except Exception as e:
        logging.error(f"Decode error: {e}")
        await update.message.reply_text("❌ មិនអាចអាន QR បានទេ", do_quote=True)


def main():
    if not TOKEN:
        print("ERROR: TELEGRAM_BOT_TOKEN is not set!")
        return

    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, generate_qr))
    app.add_handler(MessageHandler(filters.PHOTO, decode_qr))

    print("Bot Running...")
    app.run_polling()


if __name__ == "__main__":
    main()
