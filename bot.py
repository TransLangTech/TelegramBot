from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler
from handlers import start, button

# Botu oluşturma ve komutları ekleme
app = ApplicationBuilder().token("7541362503:AAFbBkSwo-kVGyN6tidha9P6b5RPqRnrlvs").build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button))

app.run_polling()
