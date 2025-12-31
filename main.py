# main.py - FINAL WhiteWhale ASCII Bot (Threaded async, no 500 errors)
import os
import logging
import threading
import asyncio
from flask import Flask, request, abort
from telegram import Update, Bot
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

BOT_TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")
SECRET_TOKEN = os.getenv("SECRET_TOKEN", "strong-secret-here")

if not BOT_TOKEN or not WEBHOOK_URL:
    raise ValueError("BOT_TOKEN and WEBHOOK_URL required!")

# Async bot application (run in background thread)
application = Application.builder().token(BOT_TOKEN).build()

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

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🌊 White Whale ASCII Bot is live! 🐋\n\n"
        "/whale YOUR MESSAGE or just type short text"
    )

async def whale_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Usage: /whale LFG")
        return
    user_text = " ".join(context.args).upper()
    await send_whale(update, user_text)

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip().upper()
    if len(text) <= 20:
        await send_whale(update, text)

async def send_whale(update: Update, user_text: str):
    if len(user_text) > 20:
        user_text = user_text[:17] + "..."
    ascii_art = WHALE_ASCII.replace("{text}", user_text.center(15))
    await update.message.reply_text(
        f"🐋 White Whale holds your sign!\n\n```ascii\n{ascii_art}\n```",
        parse_mode='Markdown'
    )

# Add handlers
application.add_handler(CommandHandler("start", start))
application.add_handler(CommandHandler("whale", whale_command))
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

# Run async function in thread
def run_async(coro):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(coro)
    loop.close()

# Set webhook at startup
def setup_webhook():
    full_url = f"{WEBHOOK_URL}/{BOT_TOKEN}"
    bot = Bot(BOT_TOKEN)
    info = asyncio.run(bot.get_webhook_info())
    if info.url != full_url:
        threading.Thread(target=run_async, args=(bot.set_webhook(url=full_url, secret_token=SECRET_TOKEN),)).start()
        logger.info(f"Webhook set to {full_url}")
    else:
        logger.info("Webhook already set")

setup_webhook()

# Webhook endpoint
@app.route(f'/{BOT_TOKEN}', methods=['POST'])
def webhook():
    if request.headers.get('X-Telegram-Bot-Api-Secret-Token') != SECRET_TOKEN:
        abort(403)
    
    json_data = request.get_json(force=True)
    update = Update.de_json(json_data, application.bot)
    
    # Process update in background thread
    threading.Thread(target=run_async, args=(application.process_update(update),)).start()
    return 'OK', 200

@app.route('/')
def index():
    return "White Whale ASCII Bot is swimming strong! 🐋"

if __name__ == '__main__':
    app.run()
