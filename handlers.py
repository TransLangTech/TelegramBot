from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from utils import get_random_word, get_quiz_options

# Botun başlangıç mesajı ve talimatları
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [
        [InlineKeyboardButton("Alıştırmaya Başla", callback_data='practice')],
        [InlineKeyboardButton("Teste Başla", callback_data='quiz')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    welcome_message = (
        f"Merhaba {update.effective_user.first_name}!\n"
        "Bu bot, YDS için en çok çıkan kelimeleri öğrenmenize yardımcı olur.\n\n"
        "Alıştırma veya test yapmak için aşağıdaki butonlardan birine tıklayabilirsiniz."
    )

    await update.message.reply_text(welcome_message, reply_markup=reply_markup)

# Kelime alıştırması başlatma
async def start_practice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    word = get_random_word()
    context.user_data['current_word'] = word
    await update.callback_query.message.reply_text(f"Kelimeyi çevirin: {word['word']}")

# Test başlatma
async def start_quiz(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    word = get_random_word()
    context.user_data['quiz_word'] = word

    options = get_quiz_options(word)
    keyboard = [[InlineKeyboardButton(opt, callback_data=f'answer_{opt}')] for opt in options]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.callback_query.message.reply_text(f"Bu kelimenin anlamı nedir: {word['word']}?", reply_markup=reply_markup)

# Kullanıcının test cevabını kontrol etme
async def check_quiz_answer(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    selected_option = query.data.split('_')[1]
    correct_answer = context.user_data['quiz_word']['translations'][0]

    if selected_option == correct_answer:
        await query.message.reply_text("Doğru! 🎉")
    else:
        await query.message.reply_text(f"Yanlış. Doğru cevap: {correct_answer}")

    await start_quiz(update, context)

# Buton tıklama işlemlerini ele alma
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    if query.data == 'practice':
        await start_practice(update, context)
    elif query.data == 'quiz':
        await start_quiz(update, context)
    elif query.data.startswith('answer_'):
        await check_quiz_answer(update, context)
