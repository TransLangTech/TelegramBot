import json
import random
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

# Kelime listesini JSON dosyasından yükleme
def load_words():
    with open("dictionary.json", "r", encoding="utf-8") as file:
        return json.load(file)

# Kelimeleri global bir değişkende saklama
words = load_words()

# Rastgele bir kelime seçme
def get_random_word():
    return random.choice(words)

# Rastgele bir kelimenin doğru cevabını ve yanlış cevap seçeneklerini alma
def get_quiz_options(correct_word):
    # Doğru cevabı alın
    correct_answer = correct_word['translations'][0]

    # Yanlış cevaplar için farklı kelimeler seç
    wrong_answers = random.sample([word['translations'][0] for word in words if word['word'] != correct_word['word']], 3)

    # Doğru cevabı ve yanlış cevapları birleştir ve karıştır
    options = wrong_answers + [correct_answer]
    random.shuffle(options)

    return options

# Botun başlangıç mesajı ve talimatları
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Butonlar oluşturuluyor
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

    # Çoktan seçmeli seçenekler oluştur
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

    # Yeni bir test başlatma
    await start_quiz(update, context)

# Buton tıklama işlemlerini ele alma
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()  # Kullanıcıya geri dönüş yapmak için gerekli

    # Butona göre işlem yapma
    if query.data == 'practice':
        await start_practice(update, context)
    elif query.data == 'quiz':
        await start_quiz(update, context)
    elif query.data.startswith('answer_'):
        await check_quiz_answer(update, context)

# Botu oluşturma ve komutları ekleme
app = ApplicationBuilder().token("Your-Token").build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button))  # Buton tıklama işlemi için handler

app.run_polling()
