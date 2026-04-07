# Telegram QR Code Bot

A Telegram bot that generates and decodes QR codes, with responses in Khmer language, plus a live web dashboard for monitoring.

## Features
- **Generate QR Code**: Send any text or URL to the bot and receive a QR code image.
- **Decode QR Code**: Send a photo of a QR code and the bot decodes its content.
- **Dashboard**: Live web dashboard showing bot status, users, and activity log.

## Tech Stack
- **Language**: Python 3.11
- **Telegram Framework**: python-telegram-bot v22.6
- **QR Generation**: qrcode v8.2 + Pillow v12.1.1
- **QR Decoding**: zbar (zbarimg system tool)
- **Dashboard**: Flask + SQLite

## Project Structure
- `main.py` - Bot logic and Telegram handlers
- `db.py` - SQLite database helpers for logging users and activities
- `dashboard.py` - Flask web dashboard on port 5000
- `templates/index.html` - Dashboard UI
- `requirements.txt` - Python dependencies
- `pyproject.toml` - Project metadata

## Configuration
- `TELEGRAM_BOT_TOKEN` - Required secret. Get one from @BotFather on Telegram.

## Workflows
- **Start application** — Runs the Telegram bot (`python main.py`), console output
- **Dashboard** — Runs the web dashboard (`python dashboard.py`) on port 5000

## System Dependencies
- `zbar` - Required for QR code decoding via `zbarimg`
