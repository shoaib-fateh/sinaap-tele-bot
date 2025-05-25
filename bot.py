from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("نقشه راه تجارت موفق", callback_data="roadmap")],
        [InlineKeyboardButton("دوره سخنرانی", callback_data="speaking")],
        [InlineKeyboardButton("دوره کسب و کار", callback_data="business")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    if update.message is not None:
        await update.message.reply_photo(
            photo="https://img.freepik.com/free-photo/person-office-analyzing-checking-finance-graphs_23-2150377127.jpg?t=st=1748085733~exp=1748089333~hmac=78018051c5fb7b2c0facfdba5c4cebbd649b9cfa196365f66bf817c99ba371be&w=826",
            caption="🎓 به ربات *سیناپ* خوش اومدی!\n\nانتخابت رو بزن و یادگیری رو شروع کن:",
            parse_mode="Markdown",
            reply_markup=reply_markup
        )

app = ApplicationBuilder().token("7767183019:AAFYKTv-SuV2pTHr1jIKF-XncgslcSGGM2w").build()
app.add_handler(CommandHandler("start", start))
app.run_polling()
