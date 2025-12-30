# whitewhale_ascii_bot.py
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Bot token from @BotFather
BOT_TOKEN = "8487247811:AAH7zkP3p8cKyc2W45bzSfQpSkGQffP6HMc"

# The ASCII art template of the White Whale holding a sign
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
        "🌊 Welcome to the White Whale ASCII Generator! 🐋\n\n"
        "Send: /whale YOUR MESSAGE\n"
        "Example: /whale LFG\n\n"
        "The mighty White Whale will hold your sign!"
    )


async def whale_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Please add a message!\nExample: /whale TO THE MOON")
        return

    user_text = " ".join(context.args).upper()

    # Limit length to avoid breaking the art
    if len(user_text) > 20:
        user_text = user_text[:17] + "..."

    # Replace {text} in the ASCII art
    ascii_art = WHALE_ASCII.replace("{text}", user_text.center(15))

    await update.message.reply_text(f"```ascii\n{ascii_art}\n```", parse_mode='Markdown')


async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip().upper()
    if len(text) <= 20 and text:  # Auto-detect short messages as potential signs
        ascii_art = WHALE_ASCII.replace("{text}", text.center(15))
        await update.message.reply_text(f"🐋 The White Whale heard your call!\n\n```ascii\n{ascii_art}\n```",
                                        parse_mode='Markdown')


def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("whale", whale_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

    print("White Whale ASCII Bot is running... 🐋")
    app.run_polling()


if __name__ == '__main__':
    main()