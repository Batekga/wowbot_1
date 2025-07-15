from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
import logging
import os
from dotenv import load_dotenv
from datetime import datetime

# Загрузка переменных окружения из файла .env
load_dotenv()

# Включение логирования
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Хранение данных
schedule_data = {}
votes = {}
group = {}
roles = {}
dungeons = {}

# Обработчик команды /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    await update.message.reply_markdown_v2(
        fr'Привет {user.mention_markdown_v2()}\! Используйте /register, чтобы отметиться, когда вы планируете играть\.'
    )

# Обработчик команды /schedule
async def schedule(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    time = context.args[0] if context.args else None
    if time:
        schedule_data[time] = schedule_data.get(time, 0) + 1
        await update.message.reply_text(f'Время {time} предложено для игры.')
    else:
        await update.message.reply_text('Пожалуйста, укажите время в формате /schedule HH:MM.')

# Обработчик команды /vote
async def vote(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    time = context.args[0] if context.args else None
    if time:
        votes[time] = votes.get(time, 0) + 1
        await update.message.reply_text(f'Вы проголосовали за время {time}.')
    else:
        await update.message.reply_text('Пожалуйста, укажите время в формате /vote HH:MM.')

# Обработчик команды /showschedule
async def showschedule(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not schedule_data:
        await update.message.reply_text('Нет предложенных времен для игры.')
    else:
        schedule_text = '\n'.join([f'Время: {time}, Предложено: {count}' for time, count in schedule_data.items()])
        await update.message.reply_text(f'Предложенные времена:\n{schedule_text}')

# Обработчик команды /remind
async def remind(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Напоминание установлено.')

# Обработчик команды /group
async def group(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    group[user.id] = user.first_name
    await update.message.reply_text(f'{user.first_name} добавлен в группу.')

# Обработчик команды /roles
async def roles(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    role = context.args[0] if context.args else None
    user = update.effective_user
    if role:
        roles[user.id] = role
        await update.message.reply_text(f'{user.first_name} выбрал роль {role}.')
    else:
        await update.message.reply_text('Пожалуйста, укажите роль в формате /roles <роль>.')

# Обработчик команды /dungeon
async def dungeon(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    dungeon_name = ' '.join(context.args)
    if dungeon_name:
        dungeons[dungeon_name] = dungeons.get(dungeon_name, 0) + 1
        await update.message.reply_text(f'Подземелье {dungeon_name} предложено для прохождения.')
    else:
        await update.message.reply_text('Пожалуйста, укажите название подземелья в формате /dungeon <название>.')

def main() -> None:
    # Получение токена из переменных окружения
    token = os.getenv('TELEGRAM_BOT_TOKEN')

    # Создание объекта Application
    application = Application.builder().token(token).build()

    # Добавление обработчиков команд
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("schedule", schedule))
    application.add_handler(CommandHandler("vote", vote))
    application.add_handler(CommandHandler("showschedule", showschedule))
    application.add_handler(CommandHandler("remind", remind))
    application.add_handler(CommandHandler("group", group))
    application.add_handler(CommandHandler("roles", roles))
    application.add_handler(CommandHandler("dungeon", dungeon))

    # Запуск бота
    application.run_polling()

if __name__ == '__main__':
    main()
