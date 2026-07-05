from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
)
import sqlite3
import random
from datetime import datetime
import config

# ==========================
# DATABASE
# ==========================

conn = sqlite3.connect("luckydraw.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS participants(
    user_id INTEGER PRIMARY KEY,
    username TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS winners(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    win_time TEXT
)
""")

conn.commit()

# ==========================
# COMMANDS
# ==========================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🎉 Welcome to Daily Lucky Draw Bot!\n\n"
        "Use /join to join the current round.\n"
        "Use /history to see previous winners."
    )


async def join(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user

    cursor.execute(
        "INSERT OR IGNORE INTO participants(user_id, username) VALUES(?,?)",
        (
            user.id,
            user.username if user.username else user.first_name
        ),
    )

    conn.commit()

    await update.message.reply_text(
        "✅ You have successfully joined this round!"
    )


async def history(update: Update, context: ContextTypes.DEFAULT_TYPE):

    cursor.execute(
        "SELECT username, win_time FROM winners ORDER BY id DESC LIMIT 10"
    )

    rows = cursor.fetchall()

    if len(rows) == 0:
        await update.message.reply_text("🏆 No winners yet.")
        return

    text = "🏆 Last 10 Winners\n\n"

    for user, time in rows:
        text += f"👤 {user}\n🕒 {time}\n\n"

    await update.message.reply_text(text)

# ==========================
# HOURLY DRAW
# ==========================

async def hourly_draw(context: ContextTypes.DEFAULT_TYPE):

    cursor.execute("SELECT user_id, username FROM participants")

    users = cursor.fetchall()

    if len(users) == 0:

        await context.bot.send_message(
            chat_id=config.CHANNEL_ID,
            text="😔 No participants joined this round."
        )

        return

    winner = random.choice(users)

    cursor.execute(
        "INSERT INTO winners(username,win_time) VALUES(?,?)",
        (
            winner[1],
            datetime.now().strftime("%d-%m-%Y %I:%M %p")
        )
    )

    conn.commit()

    cursor.execute("DELETE FROM participants")
    conn.commit()

    await context.bot.send_message(
        chat_id=config.CHANNEL_ID,
        text=f"""
🏆 DAILY LUCKY DRAW WINNER 🏆

🎉 Congratulations @{winner[1]}

🕒 {datetime.now().strftime("%I:%M %p")}

✅ New Round Started

Type /join to participate.

🎊 For Entertainment Only
"""
    )

# ==========================
# BOT
# ==========================

app = ApplicationBuilder().token(config.BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("join", join))
app.add_handler(CommandHandler("history", history))

job_queue = app.job_queue

job_queue.run_repeating(
    hourly_draw,
    interval=3600,
    first=30
)

print("Bot Running...")

app.run_polling()