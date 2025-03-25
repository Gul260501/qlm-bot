
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters, ConversationHandler

CHOOSING_TYPE, SHOW_INFO = range(2)

company_keyboard = [
    ["مسئولیت محدود (OOO)"],
    ["سهامی خاص (AO)"],
    ["کارآفرینی انفرادی (ИП)"],
    ["بازگشت به منو"]
]
company_markup = ReplyKeyboardMarkup(company_keyboard, one_time_keyboard=True, resize_keyboard=True)

company_info = {
    "مسئولیت محدود (OOO)": "شرکت مسئولیت محدود (OOO) رایج‌ترین نوع شرکت در روسیه است. مدارک مورد نیاز:\n- پاسپورت\n- آدرس اقامت\n- نوع فعالیت\n- سرمایه اولیه: حداقل 10,000 روبل",
    "سهامی خاص (AO)": "شرکت سهامی خاص (AO) مناسب فعالیت‌های بزرگ‌تر است. مدارک مورد نیاز:\n- پاسپورت\n- آدرس اقامت\n- مشخصات سهام‌داران\n- سرمایه اولیه: حداقل 100,000 روبل",
    "کارآفرینی انفرادی (ИП)": "کارآفرینی انفرادی (ИП) مخصوص افراد بدون شریک است. مدارک مورد نیاز:\n- پاسپورت\n- آدرس اقامت\n- نوع فعالیت\n- بدون نیاز به سرمایه اولیه",
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        ["ثبت شرکت در روسیه"],
        ["حسابداری و گزارش‌دهی مالی", "خدمات حقوقی و اقامتی"],
        ["تبلیغات و بازاریابی", "دریافت مشاوره"],
        ["ارسال مدارک"]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text("به ربات QLM خوش آمدید. لطفاً یک گزینه را انتخاب کنید:", reply_markup=reply_markup)

async def register_company(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("لطفاً نوع شرکت را انتخاب کنید:", reply_markup=company_markup)
    return CHOOSING_TYPE

async def choose_company_type(update: Update, context: ContextTypes.DEFAULT_TYPE):
    choice = update.message.text
    if choice == "بازگشت به منو":
        await start(update, context)
        return ConversationHandler.END
    elif choice in company_info:
        await update.message.reply_text(company_info[choice], reply_markup=company_markup)
        return SHOW_INFO
    else:
        await update.message.reply_text("لطفاً یکی از گزینه‌های معتبر را انتخاب کنید.", reply_markup=company_markup)
        return CHOOSING_TYPE

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("فرآیند لغو شد.", reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END

app = ApplicationBuilder().token("YOUR_BOT_TOKEN").build()

conv_handler = ConversationHandler(
    entry_points=[MessageHandler(filters.Regex("^ثبت شرکت در روسیه$"), register_company)],
    states={
        CHOOSING_TYPE: [MessageHandler(filters.TEXT & ~filters.COMMAND, choose_company_type)],
        SHOW_INFO: [MessageHandler(filters.TEXT & ~filters.COMMAND, choose_company_type)],
    },
    fallbacks=[CommandHandler("cancel", cancel)],
)

app.add_handler(CommandHandler("start", start))
app.add_handler(conv_handler)
