# main.py - WhiteWhale ASCII Bot (Synchronous Flask + Render compatible)
import os
import logging
import asyncio
from flask import Flask, request, abort
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Environment variables (set in Render)
BOT_TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")  # https://your-service.onrender.com
SECRET_TOKEN = os.getenv("SECRET_TOKEN", "change-this-strong-secret")

if not BOT_TOKEN or not WEBHOOK_URL:
    raise ValueError("BOT_TOKEN and WEBHOOK_URL required!")

# ASCII Whale
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

application = Application.builder().token(BOT_TOKEN).build()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🌊 Welcome to the White Whale ASCII pod! 🐋\n\n"
        "Send /whale YOUR MESSAGE\n"
        "Or type a short message — I'll hold your sign!"
    )

async def whale_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Add a message! Example: /whale LFG")
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
        f"🐋 The White Whale delivers!\n\n```ascii\n{ascii_art}\n```",
        parse_mode='Markdown'
    )

# Add handlers
application.add_handler(CommandHandler("start", start))
application.add_handler(CommandHandler("whale", whale_command))
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

# Set webhook once at startup
async def init_webhook():
    full_url = f"{WEBHOOK_URL}/{BOT_TOKEN}"
    info = await application.bot.get_webhook_info()
    if info.url != full_url:
        await application.bot.set_webhook(url=full_url, secret_token=SECRET_TOKEN)
        logger.info(f"Webhook set: {full_url}")
    else:
        logger.info("Webhook already correct")

asyncio.run(init_webhook())

@app.route(f'/{BOT_TOKEN}', methods=['POST'])
def webhook():
    if request.headers.get('X-Telegram-Bot-Api-Secret-Token') != SECRET_TOKEN:
        abort(403)
    json_data = request.get_json(force=True)
    update = Update.de_json(json_data, application.bot)
    asyncio.run(application.process_update(update))
    return 'OK', 200

@app.route('/')
def index():
    return "White Whale ASCII Bot is swimming strong! 🐋"

if __name__ == '__main__':
    app.run()
