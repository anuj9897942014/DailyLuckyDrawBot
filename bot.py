from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
)
import sqlite3
import config

# Database
conn = sqlite3.connect("luckydraw.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS participants(
    user_id INTEGER PRIMARY KEY,
    username TEXT
)
""")

conn.commit()


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🎉 Welcome to Lucky Draw Bot!\n\n"
        "Type /join to join the current lucky draw."
    )


async def join(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user

    cursor.execute(
        "INSERT OR IGNORE INTO participants(user_id, username) VALUES(?, ?)",
        (user.id, user.username or user.first_name),
    )
    conn.commit()

    await update.message.reply_text(
        "✅ You have successfully joined the current Lucky Draw!"
    )


app = ApplicationBuilder().token(config.BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("join", join))

print("Bot Running...")
app.run_polling()