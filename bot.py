from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("نقشه راه تجارت موفق", callback_data="roadmap")],
        [InlineKeyboardButton("دوره سخنرانی", callback_data="speaking")],
        [InlineKeyboardButton("دوره کسب و کار", callback_data="business")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    if update.message:
        await update.message.reply_photo(
            photo="https://img.freepik.com/free-photo/person-office-analyzing-checking-finance-graphs_23-2150377127.jpg",
            caption="🎓 به ربات *سیناپ* خوش اومدی!\n\nانتخابت رو بزن و یادگیری رو شروع کن:",
            parse_mode="Markdown",
            reply_markup=reply_markup
        )

# 🧠 هندل کردن کلیک روی دکمه‌های اول
async def handle_button_click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "roadmap":
        text = "📍 *نقشه راه تجارت موفق*\n\nدر این دوره با اصول پایه‌ی تجارت، استراتژی‌های بازاریابی و رشد کسب‌وکار آشنا می‌شی."
    elif query.data == "speaking":
        text = "🎤 *دوره سخنرانی*\n\nیاد می‌گیری چطور با اعتماد به‌نفس صحبت کنی، ذهن مخاطب رو درگیر کنی و روی صحنه بدرخشی."
    elif query.data == "business":
        text = "💼 *دوره کسب و کار*\n\nاز ایده‌پردازی تا راه‌اندازی یه بیزینس واقعی، اینجا همش رو قدم‌به‌قدم یاد می‌گیری."
    else:
        text = "😕 گزینه ناشناخته انتخاب شد."

    # ⬇️ دکمه شروع دوره
    keyboard = [[InlineKeyboardButton("🚀 شروع دوره", callback_data=f"start_{query.data}")]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.message.reply_text(text, parse_mode="Markdown", reply_markup=reply_markup)

# 🎬 وقتی روی "شروع دوره" کلیک می‌کنن
async def handle_start_course(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    course = query.data.replace("start_", "")
    await query.message.reply_text(f"✅ دوره *{course}* آغاز شد!\n\n(اینجا قراره محتوای دوره بیاد...)",
                                   parse_mode="Markdown")

# 💡 ساخت اپ و هندلرها
app = ApplicationBuilder().token("7767183019:AAFYKTv-SuV2pTHr1jIKF-XncgslcSGGM2w").build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(handle_start_course, pattern=r"^start_"))
app.add_handler(CallbackQueryHandler(handle_button_click))

app.run_polling()
