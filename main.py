
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import os

TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID", "7324306725"))

main_menu = [
    ["ثبت شرکت در روسیه", "حسابداری و گزارش‌دهی مالی"],
    ["خدمات حقوقی و اقامتی", "تبلیغات و بازاریابی"],
    ["دریافت مشاوره", "ارسال مدارک"]
]
back_menu = [["بازگشت به منو"]]

messages = {
    "welcome": "سلام! به ربات رسمی QLM خوش آمدید. لطفاً یکی از خدمات زیر را انتخاب کنید:",
    "company": "ثبت شرکت در روسیه...\n• شرکت OOO\n• شرکت ZAO\n• نمایندگی خارجی\nمدارک: پاسپورت، آدرس، نوع فعالیت",
    "accounting": "خدمات حسابداری:\n• گزارش‌های مالیاتی\n• اظهارنامه‌ها\n• حسابرسی و مشاوره",
    "legal": "خدمات اقامتی و حقوقی:\n• ویزای کاری، تحصیلی، سرمایه‌گذاری\n• اقامت موقت و دائم\n• تمدید، ثبت آدرس و...",
    "ads": "تبلیغات و بازاریابی:\n• طراحی سایت\n• سئو و Yandex Ads\n• مدیریت شبکه‌های اجتماعی",
    "consult_request": "سوال خود را بنویسید تا برای مشاوران ما ارسال شود.",
    "consult_sent": "سؤال شما برای مشاوران ارسال شد.",
    "upload": "مدارک خود را ارسال کنید. فایل‌هایی مثل PDF، Word یا عکس.",
    "thanks": "فایل شما دریافت شد. کارشناسان ما با شما تماس می‌گیرند.",
    "default": "متوجه نشدم. لطفاً یکی از گزینه‌ها را انتخاب کنید یا بازگشت بزنید."
}

user_state = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    markup = ReplyKeyboardMarkup(main_menu, resize_keyboard=True)
    await update.message.reply_text(messages["welcome"], reply_markup=markup)

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    text = update.message.text

    if user_id in user_state and user_state[user_id] == "awaiting_consult":
        user = update.message.from_user
        msg = f"سؤال جدید از {user.full_name} (@{user.username})\nآیدی: {user.id}\n\n{text}"
        await context.bot.send_message(chat_id=ADMIN_ID, text=msg)
        await update.message.reply_text(messages["consult_sent"], reply_markup=ReplyKeyboardMarkup(main_menu, resize_keyboard=True))
        user_state.pop(user_id)
        return

    replies = {
        "ثبت شرکت در روسیه": "company",
        "حسابداری و گزارش‌دهی مالی": "accounting",
        "خدمات حقوقی و اقامتی": "legal",
        "تبلیغات و بازاریابی": "ads",
        "دریافت مشاوره": "consult_request",
        "ارسال مدارک": "upload",
        "بازگشت به منو": "welcome"
    }

    key = replies.get(text)
    if key == "consult_request":
        user_state[user_id] = "awaiting_consult"
    if key:
        menu = ReplyKeyboardMarkup(main_menu if key == "welcome" else back_menu, resize_keyboard=True)
        await update.message.reply_text(messages[key], reply_markup=menu)
    else:
        await update.message.reply_text(messages["default"], reply_markup=ReplyKeyboardMarkup(main_menu, resize_keyboard=True))

async def handle_document(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    caption = f"مدرک از: {user.full_name} (@{user.username})\nآیدی: {user.id}"
    document = update.message.document
    if document:
        await context.bot.send_document(chat_id=ADMIN_ID, document=document.file_id, caption=caption)
    await update.message.reply_text(messages["thanks"])

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
app.add_handler(MessageHandler(filters.Document.ALL, handle_document))
app.run_polling()
