
from telegram import Update, ChatPermissions
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import json
import os

TOKEN = "8542672802:AAGF1qoNAN6YkGtN2iLizu1LcQCRy0hCML0"

FILTER_FILE = "filters.json"

def load_filters():
    if not os.path.exists(FILTER_FILE):
        return {}
    with open(FILTER_FILE, "r") as f:
        return json.load(f)

def save_filters(data):
    with open(FILTER_FILE, "w") as f:
        json.dump(data, f)

filters_data = load_filters()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Bot online ဖြစ်နေပါတယ် ✅")

async def add_filter(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.type == "private":
        return

    if len(context.args) < 2:
        await update.message.reply_text("သုံးပုံ: /filter word reply")
        return

    word = context.args[0].lower()
    reply = " ".join(context.args[1:])
    chat_id = str(update.effective_chat.id)

    filters_data.setdefault(chat_id, {})
    filters_data[chat_id][word] = reply
    save_filters(filters_data)

    await update.message.reply_text(f"Filter ထည့်ပြီးပါပြီ ✅ `{word}`")

async def check_filter(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text:
        return

    chat_id = str(update.effective_chat.id)
    text = update.message.text.lower()

    if chat_id in filters_data:
        for word, reply in filters_data[chat_id].items():
            if word in text:
                await update.message.reply_text(reply)
                break

async def mute(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message.reply_to_message:
        return

    user_id = update.message.reply_to_message.from_user.id
    await context.bot.restrict_chat_member(
        chat_id=update.effective_chat.id,
        user_id=user_id,
        permissions=ChatPermissions(can_send_messages=False)
    )
    await update.message.reply_text("User muted 🔇")

async def dm_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.type == "private":
        await update.message.reply_text("မင်္ဂလာပါ၊ စာလာပို့လို့ရပါတယ် 🙂")

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("filter", add_filter))
app.add_handler(CommandHandler("mute", mute))
app.add_handler(MessageHandler(filters.TEXT & filters.GROUPS, check_filter))
app.add_handler(MessageHandler(filters.TEXT & filters.PRIVATE, dm_reply))

app.run_polling()
