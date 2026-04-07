# Telegram QR Code Bot

A Telegram bot that generates and decodes QR codes, with responses in Khmer language.

## Features
- **Generate QR Code**: Send any text or URL to the bot and receive a QR code image.
- **Decode QR Code**: Send a photo of a QR code and the bot decodes its content.

## Tech Stack
- **Language**: Python 3.11
- **Telegram Framework**: python-telegram-bot v22.6
- **QR Generation**: qrcode v8.2 + Pillow v12.1.1
- **QR Decoding**: zbar (zbarimg system tool)

## Project Structure
- `main.py` - Bot logic and Telegram handlers
- `requirements.txt` - Python dependencies
- `pyproject.toml` - Project metadata

## Configuration
- `TELEGRAM_BOT_TOKEN` - Required secret. Get one from @BotFather on Telegram.

## Running
The bot runs as a console workflow (`python main.py`). It uses long-polling to receive updates from Telegram.

## System Dependencies
- `zbar` - Required for QR code decoding via `zbarimg`
