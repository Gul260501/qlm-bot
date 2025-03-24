import logging
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes, CallbackContext

import os

TOKEN = os.getenv("Bot_TOKEN")
ADMIN_ID = os.getenv("ADMIN_ID")

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

menu_keyboard = [
    ["ثبت شرکت در روسیه", "حسابداری و گزارش‌دهی مالی"],
    ["خدمات حقوقی و اقامتی", "تبلیغات و بازاریابی"],
    ["دریافت مشاوره", "ارسال مدارک"]
]
menu_markup = ReplyKeyboardMarkup(menu_keyboard, resize_keyboard=True)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("سلام! به ربات QLM خوش آمدید. لطفاً یکی از گزینه‌ها را انتخاب کنید:", reply_markup=menu_markup)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if text == "ثبت شرکت در روسیه":
        msg = (
            "لطفاً نوع شرکت را انتخاب کنید:

"
            "انواع شرکت‌ها:
"
            "• مسئولیت محدود (ООО)
"
            "• سهامی خاص (АО)
"
            "• کارآفرینی انفرادی (ИП)

"
            "مدارک مورد نیاز:
"
            "• پاسپورت
"
            "• آدرس اقامت
"
            "• نوع فعالیت
"
            "• شماره تماس روسیه"
        )
        await update.message.reply_text(msg, reply_markup=menu_markup)

    elif text == "حسابداری و گزارش‌دهی مالی":
        msg = (
            "ما خدمات حسابداری کامل از جمله:
"
            "• تهیه و ارسال گزارشات مالیاتی
"
            "• حسابداری ماهانه و سالانه
"
            "• مشاوره مالیاتی ارائه می‌دهیم.
"
            "جهت اطلاعات بیشتر لطفاً با ما تماس بگیرید."
        )
        await update.message.reply_text(msg, reply_markup=menu_markup)

    elif text == "خدمات حقوقی و اقامتی":
        msg = (
            "خدمات حقوقی و اقامتی:
"
            "• اخذ انواع اقامت روسیه
"
            "• تمدید اقامت و ویزا
"
            "• ثبت آدرس قانونی و دعوت‌نامه
"
            "• مشاوره با وکیل رسمی"
        )
        await update.message.reply_text(msg, reply_markup=menu_markup)

    elif text == "تبلیغات و بازاریابی":
        msg = (
            "خدمات تبلیغات و بازاریابی ما شامل:
"
            "• طراحی سایت و فروشگاه آنلاین
"
            "• مدیریت شبکه‌های اجتماعی
"
            "• بازاریابی محتوایی و برندینگ
"
            "• تبلیغات در پلتفرم‌های روسیه"
        )
        await update.message.reply_text(msg, reply_markup=menu_markup)

    elif text == "دریافت مشاوره":
        msg = "لطفاً سوال مشاوره‌ای خود را ارسال کنید تا کارشناسان ما با شما تماس بگیرند."
        await update.message.reply_text(msg, reply_markup=menu_markup)

    elif text == "ارسال مدارک":
        msg = "لطفاً مدارک خود را ارسال کنید. (فایل، عکس یا PDF)"
        await update.message.reply_text(msg, reply_markup=menu_markup)

    else:
        msg = "دستور نامشخص است. لطفاً یکی از گزینه‌های منو را انتخاب کنید."
        await update.message.reply_text(msg, reply_markup=menu_markup)

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    app.run_polling()