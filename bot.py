import logging
import json
from fuzzywuzzy import process
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

from config import TELEGRAM_TOKEN, TOPIC_KEYWORDS, ALL_TOPICS
from scrapers import fetch_github_trending, fetch_medium_articles

logging.basicConfig(level=logging.INFO)

# --- Helper Functions ---
def match_topic(user_input: str):
    user_input = user_input.lower().strip()
    if user_input in TOPIC_KEYWORDS:
        return TOPIC_KEYWORDS[user_input]
    match, score = process.extractOne(user_input, ALL_TOPICS)
    return match if score > 60 else None

# --- Handlers ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 ScholarMindBot is live!\n"
        "Please select your topic(s) (comma separated).\n"
        "Example: AI, Business, Programming"
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    topics = [t.strip() for t in user_text.split(",")]
    response = []

    for t in topics:
        topic = match_topic(t)
        if topic:
            response.append(f"📌 **{topic}** resources:")
            gh = await fetch_github_trending(topic.replace(" ", "").lower())
            md = await fetch_medium_articles(topic.replace(" ", "-").lower())
            response.extend(gh + md)
        else:
            response.append(f"⚠️ Unknown topic: {t}")

    await update.message.reply_text("\n".join(response))

# --- Main ---
def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()

if __name__ == "__main__":
    main()
