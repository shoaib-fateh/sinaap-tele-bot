from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)

# 🎯 دیتای دوره نقشه راه تجارت موفق
roadmap_course = [
    {
        "title": "قسمت اول: شروع از صفر",
        "desc": "توی این قسمت یاد می‌گیری چطور از هیچی، یک بیزینس بسازی.",
        "link": "https://example.com/course/start",
        "hashtags": "#تجارت #استارتاپ #یادگیری",
    },
    {
        "title": "قسمت دوم: ساخت سیستم درآمد",
        "desc": "تو باید سیستم بسازی، نه فقط کار کنی. این قسمت درباره ساختن اون سیستمه.",
        "link": "https://example.com/course/system",
        "hashtags": "#درآمد_غیرفعال #بیزینس",
    },
    {
        "title": "قسمت سوم: رشد و مقیاس‌پذیری",
        "desc": "از مشتری اول به ۱۰۰۰ تا مشتری چطور می‌رسی؟ همینجاست...",
        "link": "https://example.com/course/growth",
        "hashtags": "#مقیاس_پذیری #توسعه_کسب_و_کار",
    }
]

# 🧠 برای نگه‌داری پیشرفت هر کاربر
user_progress = {}

# 🚀 شروع ربات و نمایش دوره‌ها
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

# 🧩 هندلر کلیک روی دوره‌ها
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

# 🟢 وقتی روی "شروع دوره" کلیک میشه
async def handle_start_course(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    course = query.data.replace("start_", "")

    if course == "roadmap":
        user_id = query.from_user.id
        user_progress[user_id] = 0  # قسمت اول
        episode = roadmap_course[0]

        text = f"🎬 *{episode['title']}*\n\n{episode['desc']}\n\n{episode['hashtags']}\n🔗 {episode['link']}"
        keyboard = [[InlineKeyboardButton("⏭ قسمت بعد", callback_data="roadmap_next")]]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await query.message.reply_text(text, parse_mode="Markdown", reply_markup=reply_markup)
    else:
        await query.message.reply_text(f"✅ دوره *{course}* آغاز شد!\n\n(اینجا قراره محتوای دوره بیاد...)", parse_mode="Markdown")

# ⏭ مدیریت "قسمت بعد"
async def handle_next_roadmap(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id
    index = user_progress.get(user_id, 0) + 1

    if index < len(roadmap_course):
        user_progress[user_id] = index
        episode = roadmap_course[index]

        text = f"🎬 *{episode['title']}*\n\n{episode['desc']}\n\n{episode['hashtags']}\n🔗 {episode['link']}"
        keyboard = [[InlineKeyboardButton("⏭ قسمت بعد", callback_data="roadmap_next")]]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await query.message.reply_text(text, parse_mode="Markdown", reply_markup=reply_markup)
    else:
        await query.message.reply_text("🛠 قسمت بعدی بزودی آماده میشه!", parse_mode="Markdown")

# 🔧 ساخت اپلیکیشن و افزودن هندلرها
app = ApplicationBuilder().token("7767183019:AAFYKTv-SuV2pTHr1jIKF-XncgslcSGGM2w").build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(handle_start_course, pattern=r"^start_"))
app.add_handler(CallbackQueryHandler(handle_next_roadmap, pattern="^roadmap_next$"))
app.add_handler(CallbackQueryHandler(handle_button_click))  # این باید آخر باشه

app.run_polling()
