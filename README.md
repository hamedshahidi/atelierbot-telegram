# AtelierBot Telegram

AtelierBot is a Telegram bot + channel setup designed for a photography & videography studio in Iran.
The bot provides a tap-only experience for browsing packages, viewing samples, booking dates, and contacting the studio.

## Features (Phase 1)
- Tap-only UI (Inline keyboards + request_contact)
- Packages & pricing flow (Wedding, Birthday, Portrait)
- Samples → links to Telegram channel albums
- Booking flow (inline calendar or quick picks) + phone capture
- Contact options (call link + send my number)
- FAQ (delivery, raw files, privacy/modesty, retouching)
- Lead storage (SQLite or Google Sheets)
- Admin alerts on new leads

## Tech
- Python 3.11+
- aiogram 3.x
- python-dotenv
- SQLite (or Google Sheets)

## Quick start
```bash
python -m venv .venv
source .venv/bin/activate  # Windows Git Bash: source .venv/Scripts/activate
pip install -r requirements.txt
cp .env.example .env  # set BOT_TOKEN and ADMIN_CHAT_ID
python -m bot.app
```

## Structure
```
atelierbot-telegram/
  bot/
    app.py
    keyboards/
    handlers/
    flows/
    storage/
    texts/
    utils/
  .env.example
  requirements.txt
  README.md
```

