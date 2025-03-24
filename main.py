
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters, CallbackContext
import os

TOKEN = os.getenv("Bot_TOKEN")
ADMIN_ID = os.getenv("ADMIN_ID")

main_menu_keyboard = [
    ["ثبت شرکت در روسیه", "حسابداری و گزارش‌دهی مالی"],
    ["خدمات حقوقی و اقامتی", "تبلیغات و بازاریابی"],
    ["دریافت مشاوره", "ارسال مدارک"]
]
main_menu_markup = ReplyKeyboardMarkup(main_menu_keyboard, resize_keyboard=True)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("به ربات QLM خوش آمدید. لطفاً یکی از گزینه‌ها را انتخاب کنید:", reply_markup=main_menu_markup)

async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if text == "ثبت شرکت در روسیه":
        msg = """لطفاً نوع شرکت را انتخاب کنید:
انواع شرکت‌ها:
• مسئولیت محدود (OOO)
• سهامی خاص (AO)
• کارآفرینی انفرادی (ИП)

مدارک مورد نیاز:
• پاسپورت
• آدرس اقامت
• نوع فعالیت
• شماره تماس روسیه"""
        await update.message.reply_text(msg)

    elif text == "حسابداری و گزارش‌دهی مالی":
        msg = """خدمات حسابداری شامل:
• تهیه گزارش مالیاتی
• حقوق پرسنل
• مشاوره مالی
• ثبت دفاتر حسابرسی"""
        await update.message.reply_text(msg)

    elif text == "خدمات حقوقی و اقامتی":
        msg = """ما خدمات زیر را ارائه می‌دهیم:
• حل مشکلات ویزا
• انواع اقامت‌های کاری، تحصیلی و سرمایه‌گذاری
• ثبت آدرس حقوقی و دریافت اقامت موقت"""
        await update.message.reply_text(msg)

    elif text == "تبلیغات و بازاریابی":
        msg = """خدمات تبلیغاتی حرفه‌ای:
• طراحی سایت
• مدیریت شبکه‌های اجتماعی
• اجرای کمپین‌های تبلیغاتی آنلاین و آفلاین"""
        await update.message.reply_text(msg)

    elif text == "دریافت مشاوره":
        await update.message.reply_text("برای دریافت مشاوره، لطفاً سؤال خود را بنویسید تا کارشناسان ما پاسخ دهند.")
        return

    elif text == "ارسال مدارک":
        await update.message.reply_text("مدارک خود را ارسال کنید.
پشتیبانی از فایل‌های: PDF، عکس، Word و ...")
        return

    elif update.message.text and update.message.text != "":
        user_question = update.message.text
        await context.bot.send_message(chat_id=ADMIN_ID, text=f"سؤال مشاوره‌ای از کاربر:
{user_question}")
        await update.message.reply_text("سؤال شما برای مشاور ارسال شد. به زودی پاسخ داده خواهد شد.")

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler))

app.run_polling()
