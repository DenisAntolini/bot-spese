from google_sheets import registra_movimento, genera_riepilogo, genera_grafico
from telegram import Update, InputFile
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import logging

# Log per debug
logging.basicConfig(level=logging.INFO)

# Inserisci il tuo token
BOT_TOKEN = '8021426884:AAGX3NH3PoX1DF1QP7YGte-K15DnEAMXZ50'

# /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Ciao! Sono il bot spese familiari.\n"
        "Usa i comandi:\n"
        "/spesa 12.50 pizza\n"
        "/entrata 100 stipendio\n"
        "/riepilogo\n"
        "/grafico"
    )

# /spesa
async def spesa(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await registra(update, context, tipo="Spesa")

# /entrata
async def entrata(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await registra(update, context, tipo="Entrata")

# funzione comune
async def registra(update: Update, context: ContextTypes.DEFAULT_TYPE, tipo: str):
    try:
        args = context.args
        importo = float(args[0])
        descrizione = " ".join(args[1:]) if len(args) > 1 else "Nessuna descrizione"
        utente = update.message.from_user.first_name
        registra_movimento(utente, importo, descrizione, tipo)
        await update.message.reply_text(f"{tipo} registrata: {importo:.2f}€ - {descrizione}")
    except:
        await update.message.reply_text(f"Errore nel formato. Usa:\n/{tipo.lower()} 12.50 descrizione")

# /riepilogo
async def riepilogo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    testo = genera_riepilogo()
    await update.message.reply_text(testo)

# /grafico
async def grafico(update: Update, context: ContextTypes.DEFAULT_TYPE):
    path = genera_grafico()
    with open(path, 'rb') as f:
        await update.message.reply_photo(InputFile(f))


# Main
if __name__ == '__main__':
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("spesa", spesa))
    app.add_handler(CommandHandler("entrata", entrata))
    app.add_handler(CommandHandler("riepilogo", riepilogo))
    app.add_handler(CommandHandler("grafico", grafico))
    app.run_polling()
