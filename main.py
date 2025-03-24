
import logging
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters, CallbackContext

# تنظیمات لاگ‌ها
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# اطلاعات محیطی
import os
TOKEN = os.environ.get("Bot_TOKEN")
ADMIN_ID = os.environ.get("ADMIN_ID")

# دکمه‌های منو اصلی
main_menu_buttons = [
    ["ثبت شرکت در روسیه", "حسابداری و گزارش‌دهی مالی"],
    ["خدمات حقوقی و اقامتی", "تبلیغات و بازاریابی"],
    ["دریافت مشاوره", "ارسال مدارک"]
]

# پاسخ به /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    logging.info(f"{user.username} started the bot.")
    await update.message.reply_text(
        "به ربات QLM خوش آمدید! لطفاً یکی از گزینه‌های زیر را انتخاب کنید:",
        reply_markup=ReplyKeyboardMarkup(main_menu_buttons, resize_keyboard=True)
    )

# هندلر پیام‌های متنی
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if text == "ثبت شرکت در روسیه":
        await update.message.reply_text(
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
            "• شماره تماس روسیه
"
        )

    elif text == "حسابداری و گزارش‌دهی مالی":
        await update.message.reply_text(
            "خدمات حسابداری شامل:
"
            "• تهیه گزارش مالیاتی
"
            "• حقوق پرسنل
"
            "• مشاوره مالی"
        )

    elif text == "تبلیغات و بازاریابی":
        await update.message.reply_text(
            "ما خدمات زیر را ارائه می‌دهیم:
"
            "• طراحی سایت
"
            "• مدیریت شبکه‌های اجتماعی
"
            "• اجرای کمپین‌های تبلیغاتی"
        )

    elif text == "خدمات حقوقی و اقامتی":
        await update.message.reply_text(
            "خدمات حقوقی و اقامتی شامل:
"
            "• اقامت کاری
"
            "• ویزای تحصیلی
"
            "• تمدید اقامت و دریافت پاسپورت دوم"
        )

    elif text == "دریافت مشاوره":
        await update.message.reply_text("لطفاً سؤال خود را بنویسید تا کارشناسان ما پاسخ دهند.")
        context.user_data["awaiting_question"] = True

    elif text == "ارسال مدارک":
        await update.message.reply_text("مدارک خود را ارسال کنید. پشتیبانی از فایل‌های PDF، عکس، Word و ...")

    elif context.user_data.get("awaiting_question"):
        context.user_data["awaiting_question"] = False
        admin_message = f"سؤال مشاوره‌ای از کاربر @{update.message.from_user.username}:

{text}"
        await context.bot.send_message(chat_id=ADMIN_ID, text=admin_message)
        await update.message.reply_text("سؤال شما برای کارشناسان ما ارسال شد. به‌زودی پاسخ داده خواهد شد.")

    else:
        await update.message.reply_text("لطفاً یکی از گزینه‌های موجود را انتخاب کنید.")

# راه‌اندازی اپلیکیشن
def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    app.run_polling()

if __name__ == "__main__":
    main()
