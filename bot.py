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
import random
from datetime import datetime

async def hourly_draw(context: ContextTypes.DEFAULT_TYPE):
    cursor.execute("SELECT user_id, username FROM participants")
    users = cursor.fetchall()

    if not users:
        await context.bot.send_message(
            chat_id=config.CHANNEL_ID,
            text="😔 इस घंटे कोई भी प्रतिभागी शामिल नहीं हुआ।"
        )
        return

    winner = random.choice(users)

    cursor.execute("DELETE FROM participants")
    conn.commit()

    await context.bot.send_message(
        chat_id=config.CHANNEL_ID,
        text=f"""🏆 Lucky Draw Winner 🏆

🎉 Congratulations @{winner[1]}

⏰ {datetime.now().strftime('%I:%M %p')}

🍀 अगला Round अभी शुरू हो गया है।
For Entertainment Only."""
    )

app = ApplicationBuilder().token(config.BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("join", join))

print("Bot Running...")
app.run_polling()
job_queue = app.job_queue

job_queue.run_repeating(
    hourly_draw,
    interval=3600,
    first=10
)
