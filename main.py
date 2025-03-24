
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

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("سلام! لطفاً یکی از گزینه‌ها را انتخاب کنید:", reply_markup=ReplyKeyboardMarkup(main_menu, resize_keyboard=True))

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if text == "ثبت شرکت در روسیه":
        msg = "لطفاً نوع شرکت را انتخاب کنید:

انواع شرکت‌ها:
• مسئولیت محدود (ООО)
• سهامی خاص (АО)
• کارآفرینی انفرادی (ИП)

مدارک مورد نیاز:
• پاسپورت
• آدرس اقامت
• نوع فعالیت
• شماره تماس روسیه"
        await update.message.reply_text(msg, reply_markup=ReplyKeyboardMarkup(back_menu, resize_keyboard=True))

    elif text == "خدمات حقوقی و اقامتی":
        msg = "ما خدمات زیر را ارائه می‌دهیم:
• دریافت اقامت موقت، دائم و شهروندی
• انواع ویزا (کاری، تحصیلی، توریستی)
• مشاوره حقوقی و وکالت

برای دریافت اطلاعات بیشتر، لطفاً سوال خود را بنویسید."
        await update.message.reply_text(msg, reply_markup=ReplyKeyboardMarkup(back_menu, resize_keyboard=True))

    elif text == "حسابداری و گزارش‌دهی مالی":
        msg = "خدمات حسابداری شامل:
• تهیه گزارش مالیاتی
• حقوق پرسنل
• ثبت دفاتر حسابداری
• مشاوره مالی و مالیاتی"
        await update.message.reply_text(msg, reply_markup=ReplyKeyboardMarkup(back_menu, resize_keyboard=True))

    elif text == "تبلیغات و بازاریابی":
        msg = "خدمات ما:
• طراحی سایت و فروشگاه آنلاین
• سئو و تبلیغات در گوگل
• مدیریت شبکه‌های اجتماعی
• طراحی گرافیکی و برندینگ"
        await update.message.reply_text(msg, reply_markup=ReplyKeyboardMarkup(back_menu, resize_keyboard=True))

    elif text == "دریافت مشاوره":
        await update.message.reply_text("برای دریافت مشاوره، لطفاً سؤال خود را بنویسید تا برای کارشناسان ما ارسال شود.", reply_markup=ReplyKeyboardMarkup(back_menu, resize_keyboard=True))
        context.user_data["awaiting_question"] = True

    elif text == "ارسال مدارک":
        await update.message.reply_text("مدارک خود را ارسال کنید. پشتیبانی از فایل‌های PDF، Word، عکس و ...", reply_markup=ReplyKeyboardMarkup(back_menu, resize_keyboard=True))

    elif text == "بازگشت به منو اصلی":
        await update.message.reply_text("به منوی اصلی برگشتید. لطفاً یکی از گزینه‌ها را انتخاب کنید:", reply_markup=ReplyKeyboardMarkup(main_menu, resize_keyboard=True))

    elif context.user_data.get("awaiting_question"):
        await context.bot.send_message(chat_id=ADMIN_ID, text=f"سوال مشاوره‌ای از کاربر {update.effective_user.id}:
{text}")
        await update.message.reply_text("سوال شما ارسال شد. کارشناسان به زودی پاسخ خواهند داد.", reply_markup=ReplyKeyboardMarkup(main_menu, resize_keyboard=True))
        context.user_data["awaiting_question"] = False

    else:
        await update.message.reply_text("دستور نامشخص است. لطفاً یکی از گزینه‌ها را انتخاب کنید.", reply_markup=ReplyKeyboardMarkup(main_menu, resize_keyboard=True))

async def handle_document(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("فایل شما دریافت شد. کارشناسان ما بررسی خواهند کرد.", reply_markup=ReplyKeyboardMarkup(main_menu, resize_keyboard=True))
    await context.bot.send_document(chat_id=ADMIN_ID, document=update.message.document)

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.Document.ALL, handle_document))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

app.run_polling()
