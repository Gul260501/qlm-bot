
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import os

TOKEN = os.getenv("Bot_TOKEN")
ADMIN_ID = os.getenv("ADMIN_ID")

main_menu = [
    ["ثبت شرکت در روسیه", "حسابداری و گزارش‌دهی مالی"],
    ["خدمات حقوقی و اقامتی", "تبلیغات و بازاریابی"],
    ["دریافت مشاوره", "ارسال مدارک"]
]

back_menu = [["بازگشت به منو اصلی"]]

register_company_menu = [
    ["مسئولیت محدود (ООО)"],
    ["سهامی خاص (АО)"],
    ["کارآفرینی انفرادی (ИП)"],
    ["بازگشت به منو اصلی"]
]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("سلام! لطفاً یکی از گزینه‌ها را انتخاب کنید:", reply_markup=ReplyKeyboardMarkup(main_menu, resize_keyboard=True))

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if text == "ثبت شرکت در روسیه":
        await update.message.reply_text("لطفاً نوع شرکت را انتخاب کنید:", reply_markup=ReplyKeyboardMarkup(register_company_menu, resize_keyboard=True))

    elif text in ["مسئولیت محدود (ООО)", "سهامی خاص (АО)", "کارآفرینی انفرادی (ИП)"]:
        msg = "مدارک مورد نیاز:
• پاسپورت
• آدرس اقامت
• نوع فعالیت
• شماره تماس روسیه"
        await update.message.reply_text(msg, reply_markup=ReplyKeyboardMarkup(back_menu, resize_keyboard=True))

    elif text == "خدمات حقوقی و اقامتی":
        await update.message.reply_text(
            "در مورد خدمات حقوقی و اقامتی:
"
            "- مشاوره برای دریافت اقامت موقت و دائم
"
            "- بررسی مشکلات ویزا
"
            "- راهنمایی دریافت ویزای کاری، تحصیلی، سرمایه‌گذاری",
            reply_markup=ReplyKeyboardMarkup(back_menu, resize_keyboard=True)
        )

    elif text == "حسابداری و گزارش‌دهی مالی":
        await update.message.reply_text(
            "خدمات ما:
"
            "- تنظیم اسناد مالیاتی
"
            "- محاسبه حقوق و بیمه پرسنل
"
            "- ارائه گزارش‌های مالی ماهانه و سالانه
"
            "- مشاوره مالیاتی و مالی",
            reply_markup=ReplyKeyboardMarkup(back_menu, resize_keyboard=True)
        )

    elif text == "تبلیغات و بازاریابی":
        await update.message.reply_text(
            "خدمات تبلیغاتی:
"
            "- طراحی وب‌سایت
"
            "- مدیریت شبکه‌های اجتماعی
"
            "- اجرای کمپین‌های تبلیغاتی هدفمند",
            reply_markup=ReplyKeyboardMarkup(back_menu, resize_keyboard=True)
        )

    elif text == "دریافت مشاوره":
        await update.message.reply_text("لطفاً سؤال خود را بنویسید تا کارشناسان ما بررسی کنند.")

    elif text == "ارسال مدارک":
        await update.message.reply_text("مدارک خود را ارسال نمایید. پشتیبانی از PDF، عکس و Word.")

    elif text == "بازگشت به منو اصلی":
        await update.message.reply_text("بازگشت به منو اصلی:", reply_markup=ReplyKeyboardMarkup(main_menu, resize_keyboard=True))

    elif update.message.reply_to_message and "سؤال" in update.message.reply_to_message.text:
        await context.bot.send_message(chat_id=ADMIN_ID, text=f"سؤال مشاوره‌ای از کاربر:
{text}")
        await update.message.reply_text("سؤال شما ثبت شد. منتظر پاسخ کارشناسان باشید.")

    else:
        await update.message.reply_text("لطفاً یکی از گزینه‌های موجود را انتخاب کنید.")

async def handle_document(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("فایل شما دریافت شد. کارشناسان ما بررسی خواهند کرد.")
    await context.bot.send_document(chat_id=ADMIN_ID, document=update.message.document)

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.Document.ALL, handle_document))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
app.run_polling()
