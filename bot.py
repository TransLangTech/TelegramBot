from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler
from handlers import start, button

# Botu oluşturma ve komutları ekleme
app = ApplicationBuilder().token("Token").build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button))

app.run_polling()
