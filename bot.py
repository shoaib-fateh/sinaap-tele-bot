from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)
import html

# دیتای دوره نقشه راه تجارت موفق
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

user_progress = {}  # ذخیره وضعیت کاربر: user_id -> index

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
            caption="🎓 به ربات <b>سیناپ</b> خوش اومدی!\n\nانتخابت رو بزن و یادگیری رو شروع کن:",
            parse_mode="HTML",
            reply_markup=reply_markup
        )

async def handle_button_click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "roadmap":
        text = ("📍 <b>نقشه راه تجارت موفق</b>\n\n"
                "در این دوره با اصول پایه‌ی تجارت، استراتژی‌های بازاریابی و رشد کسب‌وکار آشنا می‌شی.")
    elif query.data == "speaking":
        text = ("🎤 <b>دوره سخنرانی</b>\n\n"
                "یاد می‌گیری چطور با اعتماد به‌نفس صحبت کنی، ذهن مخاطب رو درگیر کنی و روی صحنه بدرخشی.")
    elif query.data == "business":
        text = ("💼 <b>دوره کسب و کار</b>\n\n"
                "از ایده‌پردازی تا راه‌اندازی یه بیزینس واقعی، اینجا همش رو قدم‌به‌قدم یاد می‌گیری.")
    else:
        text = "😕 گزینه ناشناخته انتخاب شد."

    keyboard = [[InlineKeyboardButton("🚀 شروع دوره", callback_data=f"start_{query.data}")]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.message.reply_text(text, parse_mode="HTML", reply_markup=reply_markup)

async def handle_start_course(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    course = query.data.replace("start_", "")

    if course == "roadmap":
        user_id = query.from_user.id
        user_progress[user_id] = 0  # شروع از قسمت اول
        await send_roadmap_part(query, user_id, 0)
    else:
        await query.message.reply_text(f"✅ دوره <b>{html.escape(course)}</b> آغاز شد!\n\n(محتوا بزودی اضافه می‌شود)", parse_mode="HTML")

async def send_roadmap_part(query, user_id, index):
    episode = roadmap_course[index]
    text = (
        f"🎬 <b>{html.escape(episode['title'])}</b>\n\n"
        f"{html.escape(episode['desc'])}\n\n"
        f"{html.escape(episode['hashtags'])}\n"
        f"🔗 <a href='{episode['link']}'>لینک دوره</a>\n\n"
        f"🔹 <b>قسمت {index + 1} از {len(roadmap_course)}</b>"
    )

    keyboard_buttons = []
    # دکمه قسمت قبل
    if index > 0:
        keyboard_buttons.append(InlineKeyboardButton("⬅️ قسمت قبل", callback_data="roadmap_prev"))
    # دکمه قسمت بعد
    if index < len(roadmap_course) - 1:
        keyboard_buttons.append(InlineKeyboardButton("➡️ قسمت بعد", callback_data="roadmap_next"))

    reply_markup = InlineKeyboardMarkup([keyboard_buttons]) if keyboard_buttons else None

    # پیام رو ویرایش کن (edit_message_text) به جای ارسال جدید، برای کم کردن لگ و اسپم
    await query.message.edit_text(text, parse_mode="HTML", reply_markup=reply_markup, disable_web_page_preview=False)

async def handle_roadmap_navigation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    current_index = user_progress.get(user_id, 0)

    if query.data == "roadmap_next":
        if current_index < len(roadmap_course) - 1:
            current_index += 1
            user_progress[user_id] = current_index
    elif query.data == "roadmap_prev":
        if current_index > 0:
            current_index -= 1
            user_progress[user_id] = current_index

    await send_roadmap_part(query, user_id, current_index)

# ساخت اپلیکیشن و هندلرها
app = ApplicationBuilder().token("7767183019:AAFYKTv-SuV2pTHr1jIKF-XncgslcSGGM2w").build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(handle_start_course, pattern=r"^start_"))
app.add_handler(CallbackQueryHandler(handle_roadmap_navigation, pattern="^roadmap_(next|prev)$"))
app.add_handler(CallbackQueryHandler(handle_button_click))  # این باید آخر باشه

app.run_polling()
