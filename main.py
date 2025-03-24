
import os
from telegram import Update, ReplyKeyboardMarkup, Document
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))

messages = {
    "welcome": "سلام! به ربات رسمی QLM خوش آمدید. لطفاً یکی از خدمات زیر را انتخاب کنید:",
    "company": "لطفاً نوع شرکت را انتخاب کنید:",
    "company_types": "انواع شرکت‌ها:\n• مسئولیت محدود (OOO)\n• سهامی خاص (АО)\n• کارآفرینی انفرادی (ИП)\n\nمدارک مورد نیاز:\n• پاسپورت\n• آدرس اقامت\n• نوع فعالیت\n• شماره تماس روسیه",
    "accounting": "خدمات حسابداری ما شامل:\n• گزارش‌دهی مالیاتی\n• مدیریت حقوق و دستمزد\n• مشاوره مالی و مالیاتی\n• افتتاح حساب بانکی شرکتی",
    "legal": "خدمات حقوقی و مهاجرتی ما شامل:\n• اقامت کاری و تحصیلی\n• ویزای کار، تحصیل و سرمایه‌گذاری\n• رفع مشکلات ریجکتی و تمدید اقامت",
    "ads": "ما خدمات حرفه‌ای تبلیغات ارائه می‌دهیم:\n• طراحی سایت\n• مدیریت اینستاگرام و تلگرام\n• اجرای کمپین‌های هدفمند تبلیغاتی",
    "consult": "برای دریافت مشاوره، لطفاً سوال خود را بنویسید. کارشناسان ما پاسخ خواهند داد.",
    "upload": "مدارک خود را ارسال کنید. فرمت‌های قابل قبول: PDF، Word، تصویر.",
    "thanks": "مدرک شما دریافت شد. کارشناسان ما بررسی خواهند کرد.",
    "back": "به منوی اصلی برگشتید. یکی از گزینه‌ها را انتخاب کنید.",
    "default": "دستور نامشخص است. لطفاً یکی از گزینه‌ها را از منو انتخاب کنید."
}

keyboards = [
    ["ثبت شرکت در روسیه", "حسابداری و گزارش‌دهی مالی"],
    ["خدمات حقوقی و اقامتی", "تبلیغات و بازاریابی"],
    ["دریافت مشاوره", "ارسال مدارک"],
    ["بازگشت به منوی اصلی"]
]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    markup = ReplyKeyboardMarkup(keyboards, resize_keyboard=True)
    await update.message.reply_text(messages["welcome"], reply_markup=markup)

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if text == "ثبت شرکت در روسیه":
        await update.message.reply_text(messages["company"])
        await update.message.reply_text(messages["company_types"])
    elif text == "حسابداری و گزارش‌دهی مالی":
        await update.message.reply_text(messages["accounting"])
    elif text == "خدمات حقوقی و اقامتی":
        await update.message.reply_text(messages["legal"])
    elif text == "تبلیغات و بازاریابی":
        await update.message.reply_text(messages["ads"])
    elif text == "دریافت مشاوره":
        await update.message.reply_text(messages["consult"])
    elif text == "ارسال مدارک":
        await update.message.reply_text(messages["upload"])
    elif text == "بازگشت به منوی اصلی":
        await start(update, context)
    else:
        await update.message.reply_text(messages["default"])

async def handle_document(update: Update, context: ContextTypes.DEFAULT_TYPE):
    file = update.message.document
    await update.message.reply_text(messages["thanks"])
    await context.bot.forward_message(chat_id=ADMIN_ID, from_chat_id=update.message.chat_id, message_id=update.message.message_id)

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
app.add_handler(MessageHandler(filters.Document.ALL, handle_document))

if __name__ == "__main__":
    print("ربات QLM آماده اجراست...")
    app.run_polling()
