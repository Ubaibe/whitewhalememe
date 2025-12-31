# main.py - WhiteWhale ASCII Webhook Bot (Render-compatible, PTB v22+)
import os
import logging
from flask import Flask, request, abort
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import asyncio

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Environment variables - set these in Render dashboard
BOT_TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")  # e.g. https://your-service.onrender.com
SECRET_TOKEN = os.getenv("SECRET_TOKEN", "change-this-to-something-strong")

if not BOT_TOKEN or not WEBHOOK_URL:
    raise ValueError("BOT_TOKEN and WEBHOOK_URL must be set!")

# ASCII Whale template
WHALE_ASCII = """
               ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
            ▓▓▓▓▓▓████████████▓▓▓▓▓
          ▓▓▓▓████████████████████▓▓▓
        ▓▓▓██████████████████████████▓▓
       ▓██████████████████████████████▓
      ▓████████████████████████████████▓
     ▓██████████████████████████████████▓
    ▓████████████████████████████████████▓
   ▓██████████████████████████████████████▓
  ▓████████████████████████████████████████▓
 ▓██████████████████████████████████████████▓
 ▓██████████████████████████████████████████▓
▓████████████████████████████████████████████▓
▓████████████████████████████████████████████▓
▓████████████████████████████████████████████▓
 ▓██████████████████████████████████████████▓
  ▓████████████████████████████████████████▓
   ▓██████████████████████████████████████▓
    ▓████████████████████████████████████▓
     ▓██████████████████████████████████▓
      ▓████████████████████████████████▓
       ▓██████████████████████████████▓
        ▓▓██████████████████████████▓▓
          ▓▓▓████████████████████▓▓▓
            ▓▓▓▓████████████████▓▓▓
               ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
                  /| ________
                 / |/        \\
                /  ||   {text}   ||
               /   ||         ||
              /    ||_________||
             /      \\         /
            /        \\_______/
"""

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🌊 Welcome aboard, captain! 🐋\n\n"
        "Send /whale YOUR MESSAGE\n"
        "Or just type a short message (up to 20 chars) and the White Whale will hold your sign!\n\n"
        "Example: /whale LFG"
    )

async def whale_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Add a message! Example: /whale TO THE MOON")
        return
    user_text = " ".join(context.args).upper()
    await send_whale(update, user_text)

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip().upper()
    if len(text) <= 20 and text:
        await send_whale(update, text)

async def send_whale(update: Update, user_text: str):
    if len(user_text) > 20:
        user_text = user_text[:17] + "..."
    ascii_art = WHALE_ASCII.replace("{text}", user_text.center(15))
    await update.message.reply_text(
        f"🐋 The White Whale carries your message!\n\n```ascii\n{ascii_art}\n```",
        parse_mode='Markdown'
    )

# Create PTB Application
application = Application.builder().token(BOT_TOKEN).build()

# Add handlers
application.add_handler(CommandHandler("start", start))
application.add_handler(CommandHandler("whale", whale_command))
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

# Set webhook on first request (runs in the request's async context)
async def ensure_webhook():
    webhook_path = f"/{BOT_TOKEN}"
    full_url = f"{WEBHOOK_URL}{webhook_path}"
    info = await application.bot.get_webhook_info()
    if info.url != full_url:
        await application.bot.set_webhook(url=full_url, secret_token=SECRET_TOKEN)
        logger.info(f"Webhook set to {full_url}")
    else:
        logger.info("Webhook already set correctly")

@app.route(f'/{BOT_TOKEN}', methods=['POST'])
async def webhook():
    # Security check
    if request.headers.get('X-Telegram-Bot-Api-Secret-Token') != SECRET_TOKEN:
        abort(403)

    # Ensure webhook is set (first request or if changed)
    await ensure_webhook()

    # Process update
    json_data = request.get_json(force=True)
    update = Update.de_json(json_data, application.bot)
    await application.process_update(update)
    return 'OK', 200

@app.route('/')
def index():
    return "White Whale ASCII Bot is swimming strong! 🐋"

if __name__ == '__main__':
    app.run()
