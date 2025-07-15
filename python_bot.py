from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
import logging
import os
from dotenv import load_dotenv

# Загрузка переменных окружения из файла .env
load_dotenv()

# Включение логирования
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Обработчик команды /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    await update.message.reply_markdown_v2(
        fr'Привет {user.mention_markdown_v2()}\! Используйте /register, чтобы отметиться, когда вы планируете играть\.'
    )

# Обработчик команды /register
async def register(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [
        [InlineKeyboardButton("Сейчас", callback_data='now'),
         InlineKeyboardButton("Через 1 час", callback_data='1_hour'),
         InlineKeyboardButton("Через 2 часа", callback_data='2_hours')],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text('Пожалуйста, выберите, когда вы планируете играть:', reply_markup=reply_markup)

# Обработчик нажатий на кнопки
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    # Получение данных о времени
    time_chosen = query.data
    user = query.from_user

    # Сообщение об успешной регистрации
    await query.edit_message_text(text=f"{user.first_name} отметился, что будет играть {get_time_text(time_chosen)}.")

# Вспомогательная функция для получения текста времени
def get_time_text(time_data):
    time_texts = {
        'now': 'сейчас',
        '1_hour': 'через 1 час',
        '2_hours': 'через 2 часа',
    }
    return time_texts.get(time_data, 'в неизвестное время')

def main() -> None:
    # Получение токена из переменных окружения
    token = os.getenv('TELEGRAM_BOT_TOKEN')

    # Создание объекта Application
    application = Application.builder().token(token).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("register", register))
    application.add_handler(CallbackQueryHandler(button))

    # Запуск бота
    application.run_polling()

if __name__ == '__main__':
    main()
