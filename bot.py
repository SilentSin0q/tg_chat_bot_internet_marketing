import logging
from datetime import datetime

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

# Вставьте сюда токен от BotFather
TOKEN = "8867557774:AAGlur_ygcP34o-o9bzvaVYim4HgivshQHQ"

# Логирование
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

# База FAQ
FAQ = {
    "доставка": "🚚 Доставка занимает от 1 до 5 рабочих дней.",
    "оплата": "💳 Мы принимаем банковские карты и электронные платежи.",
    "возврат": "↩️ Возврат возможен в течение 14 дней после получения товара.",
    "контакты": "📞 Телефон поддержки: +7 (999) 123-45-67."
}


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"Пользователь {update.effective_user.username} запустил бота")

    await update.message.reply_text(
        "Здравствуйте! 👋\n\n"
        "Я бот-консультант.\n\n"
        "Могу помочь:\n"
        "• с вопросами по доставке\n"
        "• с оплатой\n"
        "• с возвратом\n"
        "• оформить заказ\n\n"
        "Напишите свой вопрос."
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Доступные команды:\n"
        "/start - запуск бота\n"
        "/help - помощь"
    )


def save_order(user_name, text):
    with open("orders.txt", "a", encoding="utf-8") as file:
        file.write(
            f"\n{'=' * 40}\n"
            f"Дата: {datetime.now()}\n"
            f"Пользователь: {user_name}\n"
            f"Заказ: {text}\n"
        )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower()

    print(f"Сообщение: {text}")

    # FAQ
    for keyword, answer in FAQ.items():
        if keyword in text:
            await update.message.reply_text(answer)
            return

    # Заказ
    if "заказ" in text:
        save_order(
            update.effective_user.username,
            update.message.text
        )

        await update.message.reply_text(
            "✅ Ваша заявка принята.\n\n"
            "Для оформления заказа отправьте:\n"
            "1. Название товара\n"
            "2. Количество\n"
            "3. Адрес доставки\n"
            "4. Контактный телефон"
        )
        return

    # Консультация
    if any(word in text for word in [
        "помощь",
        "консультация",
        "совет",
        "подобрать"
    ]):
        await update.message.reply_text(
            "🛍 Опишите товар или услугу, которая вас интересует, "
            "и я постараюсь помочь."
        )
        return

    await update.message.reply_text(
        "Я пока не знаю ответа на этот вопрос.\n"
        "Попробуйте написать:\n"
        "• доставка\n"
        "• оплата\n"
        "• возврат\n"
        "• заказ"
    )


async def error_handler(update, context):
    print("Ошибка:", context.error)


def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))

    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            handle_message
        )
    )

    app.add_error_handler(error_handler)

    print("Бот успешно запущен...")
    app.run_polling(drop_pending_updates=True)


if __name__ == "__main__":
    main()