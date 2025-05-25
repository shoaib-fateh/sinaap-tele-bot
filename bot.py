from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)
import html

# داده‌های دوره‌ی "نقشه راه تجارت موفق"
roadmap_course = [
    {
        "title": "قسمت اول: شروع از صفر",
        "desc": "توی این قسمت یاد می‌گیری چطور از هیچی، یک بیزینس بسازی.",
        "link": "https://example.com/course/start",
        "hashtags": "#تجارت #استارتاپ #یادگیری",
        "video": "https://cdn.pixabay.com/video/2025/05/13/278750_large.mp4"
    },
    {
        "title": "قسمت دوم: ساخت سیستم درآمد",
        "desc": "تو باید سیستم بسازی، نه فقط کار کنی. این قسمت درباره ساختن اون سیستمه.",
        "link": "https://example.com/course/system",
        "hashtags": "#درآمد_غیرفعال #بیزینس",
        "video": "https://cdn.pixabay.com/video/2023/12/12/192935-893872011_large.mp4"
    },
    {
        "title": "قسمت سوم: رشد و مقیاس‌پذیری",
        "desc": "از مشتری اول به ۱۰۰۰ تا مشتری چطور می‌رسی؟ همینجاست...",
        "link": "https://example.com/course/growth",
        "hashtags": "#مقیاس_پذیری #توسعه_کسب_و_کار",
        "video": "https://cdn.pixabay.com/video/2016/02/15/2176-155747466_large.mp4"
    }
]

# وضعیت مشاهده کاربران در دوره‌ها
user_progress = {}  # user_id -> episode_index


# فرمان /start: معرفی ربات و دوره‌ها
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


# کلیک روی دکمه‌های معرفی دوره‌ها
async def handle_button_click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    course_texts = {
        "roadmap": ("📍 <b>نقشه راه تجارت موفق</b>\n\n"
                    "در این دوره با اصول پایه‌ی تجارت، استراتژی‌های بازاریابی و رشد کسب‌وکار آشنا می‌شی."),
        "speaking": ("🎤 <b>دوره سخنرانی</b>\n\n"
                     "یاد می‌گیری چطور با اعتماد به‌نفس صحبت کنی، ذهن مخاطب رو درگیر کنی و روی صحنه بدرخشی."),
        "business": ("💼 <b>دوره کسب و کار</b>\n\n"
                     "از ایده‌پردازی تا راه‌اندازی یه بیزینس واقعی، اینجا همش رو قدم‌به‌قدم یاد می‌گیری.")
    }

    text = course_texts.get(query.data, "😕 گزینه ناشناخته انتخاب شد.")
    keyboard = [[InlineKeyboardButton("🚀 شروع دوره", callback_data=f"start_{query.data}")]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.message.reply_text(text, parse_mode="HTML", reply_markup=reply_markup)


# شروع هر دوره
async def handle_start_course(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    course = query.data.replace("start_", "")
    user_id = query.from_user.id

    if course == "roadmap":
        user_progress[user_id] = 0
        await send_roadmap_part(query, user_id, 0)
    else:
        await query.message.reply_text(
            f"✅ دوره <b>{html.escape(course)}</b> آغاز شد!\n\n(محتوا بزودی اضافه می‌شود)",
            parse_mode="HTML"
        )


# ارسال قسمت مشخص از دوره roadmap
async def send_roadmap_part(query, user_id, index):
    episode = roadmap_course[index]

    caption = (
        f"🎬 <b>{html.escape(episode['title'])}</b>\n\n"
        f"{html.escape(episode['desc'])}\n\n"
        f"{html.escape(episode['hashtags'])}\n"
        f"🔹 <b>قسمت {index + 1} از {len(roadmap_course)}</b>"
    )

    nav_buttons = []
    if index > 0:
        nav_buttons.append(InlineKeyboardButton("⬅️ قسمت قبل", callback_data="roadmap_prev"))
    if index < len(roadmap_course) - 1:
        nav_buttons.append(InlineKeyboardButton("➡️ قسمت بعد", callback_data="roadmap_next"))

    reply_markup = InlineKeyboardMarkup([nav_buttons]) if nav_buttons else None

    try:
        await query.message.delete()
    except:
        pass

    await query.message.reply_video(
        video=episode["video"],
        caption=caption,
        parse_mode="HTML",
        reply_markup=reply_markup
    )


# کنترل دکمه‌های قبلی / بعدی دوره roadmap
async def handle_roadmap_navigation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    current_index = user_progress.get(user_id, 0)

    if query.data == "roadmap_next" and current_index < len(roadmap_course) - 1:
        current_index += 1
    elif query.data == "roadmap_prev" and current_index > 0:
        current_index -= 1

    user_progress[user_id] = current_index
    await send_roadmap_part(query, user_id, current_index)


# اجرای ربات
def main():
    app = ApplicationBuilder().token("7767183019:AAFYKTv-SuV2pTHr1jIKF-XncgslcSGGM2w").build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(handle_start_course, pattern=r"^start_"))
    app.add_handler(CallbackQueryHandler(handle_roadmap_navigation, pattern=r"^roadmap_(next|prev)$"))
    app.add_handler(CallbackQueryHandler(handle_button_click))  # باید آخر باشه

    print("✅ Bot is running...")
    app.run_polling()


if __name__ == "__main__":
    main()
