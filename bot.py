BOT_TOKEN = ""

from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters

TOKEN = "7431332809:AAEKuhntXgihb_KbHdfBrR3vGAzfxOx4eeI"  # Лучше использовать переменные окружения!

async def start(update: Update, context):
    await update.message.reply_text("Привет! Я бот на Railway!")

if __name__ == "__main__":
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.run_polling()  # Long-polling (не требует вебхука)