from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import logging
import os

# تنظیمات پایه
BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))

logging.basicConfig(level=logging.INFO)

# پیام‌ها
messages = {
    "welcome": "سلام! لطفاً یکی از خدمات زیر را انتخاب کنید:",
    "back": "بازگشت به منوی اصلی انجام شد.",
    "unknown": "در حال حاضر متوجه منظورتان نشدم. لطفاً از گزینه‌ها استفاده کنید.",
}

# منوها
main_menu = [
    ["ثبت شرکت در روسیه", "حسابداری و گزارش‌دهی مالی"],
    ["خدمات حقوقی و اقامتی", "تبلیغات و بازاریابی"],
    ["دریافت مشاوره", "ارسال مدارک"]
]

submenus = {
    "ثبت شرکت در روسیه": [
        ["مسئولیت محدود (OOO)"], ["سهامی خاص (ZAO)"], ["فردی (IP)"], ["بازگشت به منو"]
    ],
    "خدمات حقوقی و اقامتی": [
        ["اقامت موقت / دائم"], ["ویزای کاری، تحصیلی، تجاری"], ["تمدید ویزا / رفع ریجکتی"], ["بازگشت به منو"]
    ],
    "حسابداری و گزارش‌دهی مالی": [
        ["گزارش مالیاتی"], ["حقوق و بیمه پرسنل"], ["مشاوره مالی"], ["بازگشت به منو"]
    ],
    "تبلیغات و بازاریابی": [
        ["طراحی سایت"], ["مدیریت شبکه‌های اجتماعی"], ["کمپین‌های تبلیغاتی"], ["بازگشت به منو"]
    ],
}

# پیام‌های زیرمنو
submenu_messages = {
    "مسئولیت محدود (OOO)": "برای ثبت شرکت OOO مدارک موردنیاز: پاسپورت، آدرس، نوع فعالیت.",
    "سهامی خاص (ZAO)": "برای شرکت ZAO باید حداقل 2 سهام‌دار معرفی شوند.",
    "فردی (IP)": "ثبت شرکت فردی برای یک نفر و ساده‌تر است.",
    "اقامت موقت / دائم": "ما در دریافت اقامت موقت و دائم همراه شما هستیم.",
    "ویزای کاری، تحصیلی، تجاری": "برای اخذ ویزا، مدارک لازم را ارسال نمایید.",
    "تمدید ویزا / رفع ریجکتی": "برای تمدید ویزا یا رفع ریجکتی، با ما در تماس باشید.",
    "گزارش مالیاتی": "ما گزارش مالیاتی ماهانه و سالانه تهیه می‌کنیم.",
    "حقوق و بیمه پرسنل": "تهیه لیست حقوق و بیمه با استانداردهای روسیه.",
    "مشاوره مالی": "دریافت مشاوره مالی با کارشناسان خبره.",
    "طراحی سایت": "طراحی وب‌سایت شرکتی، فروشگاهی، چندزبانه.",
    "مدیریت شبکه‌های اجتماعی": "برنامه‌ریزی و اجرای محتوا و تبلیغات.",
    "کمپین‌های تبلیغاتی": "اجرای تبلیغات حرفه‌ای در گوگل، یندکس و اینستاگرام.",
}

# استارت
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    markup = ReplyKeyboardMarkup(main_menu, resize_keyboard=True)
    await update.message.reply_text(messages["welcome"], reply_markup=markup)

# دریافت پیام‌ها
async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    user = update.message.from_user
    uid = user.id

    logging.info(f"{uid} | {user.first_name} | sent: {text}")

    if text == "بازگشت به منو":
        markup = ReplyKeyboardMarkup(main_menu, resize_keyboard=True)
        await update.message.reply_text(messages["back"], reply_markup=markup)
        return

    for section, options in submenus.items():
        if text == section:
            markup = ReplyKeyboardMarkup(options, resize_keyboard=True)
            await update.message.reply_text("لطفاً یکی از گزینه‌های زیر را انتخاب کنید:", reply_markup=markup)
            return

    if text in submenu_messages:
        await update.message.reply_text(submenu_messages[text])
        return

    if text == "دریافت مشاوره":
        await update.message.reply_text("لطفاً سؤال خود را بنویسید تا برای کارشناسان ما ارسال شود.")
        context.user_data["awaiting_question"] = True
        return

    if context.user_data.get("awaiting_question"):
        context.user_data["awaiting_question"] = False
        msg = f"سؤال مشاوره‌ای از کاربر:

🧑‍💼 نام: {user.full_name}
🆔 آیدی: {uid}

❓ سؤال:
{text}"
        await context.bot.send_message(chat_id=ADMIN_ID, text=msg)
        await update.message.reply_text("سؤال شما ثبت شد. به زودی با شما تماس خواهیم گرفت.")
        return

    if text == "ارسال مدارک":
        await update.message.reply_text("لطفاً مدارک خود را ارسال نمایید. (PDF، عکس، Word)")
        return

    await update.message.reply_text(messages["unknown"])

# دریافت فایل
async def handle_document(update: Update, context: ContextTypes.DEFAULT_TYPE):
    doc = update.message.document
    user = update.message.from_user
    await context.bot.send_document(chat_id=ADMIN_ID, document=doc.file_id,
        caption=f"مدرک از {user.full_name} ({user.id})")
    await update.message.reply_text("مدرک شما دریافت شد. کارشناسان به زودی با شما تماس می‌گیرند.")

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
app.add_handler(MessageHandler(filters.Document.ALL, handle_document))

print("ربات پیشرفته QLM آماده اجراست...")
app.run_polling()
