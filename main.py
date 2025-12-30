# main.py - WhiteWhale ASCII Webhook Bot for Render
from flask import Flask, request, abort
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import asyncio
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Get from environment variables (set these in Render dashboard)
BOT_TOKEN = "8487247811:AAH7zkP3p8cKyc2W45bzSfQpSkGQffP6HMc"
WEBHOOK_URL = "https://whitewhalememe.onrender.com"  # https://your-app.onrender.com

# Secret token to validate Telegram requests (optional but recommended)
# SECRET_TOKEN = os.getenv("SECRET_TOKEN", "super-secret-token-change-this")

# The ASCII whale template
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

# Flask route for Telegram webhook
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

# Global application
application = None

@app.before_first_request
def setup_bot():
    global application
    loop = asyncio.get_event_loop()
    
    application = Application.builder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("whale", whale_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

    # Set webhook
    loop.run_until_complete(application.bot.set_webhook(url=f"{WEBHOOK_URL}/{BOT_TOKEN}"))
    logger.info(f"Webhook set to {WEBHOOK_URL}/{BOT_TOKEN}")

if __name__ == '__main__':
    # For local testing
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

