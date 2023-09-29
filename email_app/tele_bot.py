import telegram
from telegram import ForceReply, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
import os
import dotenv
import sys
from . import email_predict
import json

# Store all message IDs
all_message_ids = []

async def store_message_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_id = update.message.message_id
    all_message_ids.append(message_id)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    await update.message.reply_html(f"Hello {user.mention_html()}!, Welcome to the k3s home server notification groupchat.")

async def get_chat_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    await update.message.reply_text(f"The chat ID of this group is {chat_id}")

async def predict(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Predicting emails may take up to 5 mins...")
    email_predict.main()
    await update.message.reply_text("emails predicted")


async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = "1) To get chat id type /chatid.\n \
        2) To get all email predictions type /e-predict."
    await update.message.reply_text(text)

async def get_all_message_ids(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"All Message IDs: {', '.join(map(str, all_message_ids))}")

async def clear_history(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Get the chat ID and message ID
    chat_id = update.message.chat_id
    message_id = update.message.message_id

    # Iterate through the messages sent by the bot and delete them
    async for message in context.bot.iter_chat_messages(chat_id, from_user=context.bot.id):
        await message.delete()

    # Inform the user that the chat history has been cleared
    await update.message.reply_text("Bot's messages have been cleared.")

def get_token():
    dir_name = os.getcwd()
    env_path = os.path.join(dir_name, ".env")
    dotenv.load_dotenv(env_path)

    return {
        't': os.environ.get("TOKEN")
    }

def main():
    cred = get_token()
    t = cred['t']
    print(t)

    app = Application.builder().token(t).build()

    app.add_handler(MessageHandler(filters.TEXT & filters.COMMAND, store_message_id))
    app.add_handler(CommandHandler('start', start))
    app.add_handler(CommandHandler('chatid', get_chat_id))
    app.add_handler(CommandHandler('epredict', predict))
    app.add_handler(CommandHandler('help', help))
    app.add_handler(CommandHandler('clear', clear_history))
    app.add_handler(CommandHandler('getallmessageids', get_all_message_ids))

    try:
        app.run_polling()
    except KeyboardInterrupt:
        print("Bot stopped.")