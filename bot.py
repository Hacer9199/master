from telegram import Update
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes,
    ConversationHandler, filters
)

TOKEN = "7595760258:AAEUPUeST3m2HTgXvyZg-mohSYb3EVmLcbY"  # ← Токени худро гузоред

NAME, PHONE, ORDER = range(3)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Салом! Барои фармоиш, аввал номи худро нависед:")
    return NAME

async def get_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["name"] = update.message.text
    await update.message.reply_text("Сипос! Ҳоло рақами телефони худро нависед:")
    return PHONE

async def get_phone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["phone"] = update.message.text
    await update.message.reply_text("Фармоиши худро нависед (HTML, сайт сохтан ва ғайра):")
    return ORDER

async def get_order(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["order"] = update.message.text

    name = context.user_data["name"]
    phone = context.user_data["phone"]
    order = context.user_data["order"]
    user_id = update.message.from_user.id  # ИД-и корбар

    result = (
        f"📥 Фармоиши нав:\n"
        f"👤 Ном: {name}\n"
        f"📞 Телефон: {phone}\n"
        f"📄 Хизмат: {order}\n"
        f"🆔 ID-и корбар: {user_id}"
    )

    await update.message.reply_text("Фармоиши шумо қабул шуд. Мо ба шумо менависем!\n\n" + result)

    ADMIN_ID = 1860232019  # ← ID-и худатонро гузоред
    await context.bot.send_message(chat_id=ADMIN_ID, text=result)

    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Фармоиш қатъ карда шуд.")
    return ConversationHandler.END

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_name)],
            PHONE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_phone)],
            ORDER: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_order)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    app.add_handler(conv_handler)
    print("✅ Бот барои қабул кардани заказ фаъол аст.")
    app.run_polling()

if __name__ == "__main__":
    main()
