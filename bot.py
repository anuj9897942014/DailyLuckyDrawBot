from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import random

BOT_TOKEN = "YAHAN_APNA_BOT_TOKEN_DALO"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🎉 Welcome to Daily Lucky Draw Bot!\n\n"
        "Commands:\n"
        "/luck - Get your lucky number\n"
        "/help - Help"
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "/luck - Generate your lucky number (1-100)"
    )

async def luck(update: Update, context: ContextTypes.DEFAULT_TYPE):
    number = random.randint(1, 100)
    await update.message.reply_text(
        f"🍀 Your Lucky Number is: {number}"
    )

app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("help", help_command))
app.add_handler(CommandHandler("luck", luck))

print("Bot is running...")
app.run_polling()
