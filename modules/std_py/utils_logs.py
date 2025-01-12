import os
from datetime import datetime

# Константы
LOGS_DIR = "logs"  # Папка для логов
LOG_SESSION_FILE = os.path.join(LOGS_DIR, "log_session.txt")  # Лог текущей сессии
LOG_ALL_FILE = os.path.join(LOGS_DIR, "log_all.txt")  # Лог всей истории

# Создаем папку logs, если она не существует
if not os.path.exists(LOGS_DIR):
    os.makedirs(LOGS_DIR)

def log_message(message, log_file):
    """Логирует сообщение в указанный файл с кодировкой UTF-8."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] {message}\n"
    with open(log_file, "a", encoding="utf-8") as file:
        file.write(log_entry)

def log_command_and_result(command, result, username):
    """Логирует команду, результат и пользователя."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] Пользователь: {username}, Команда: {command}, Результат: {result}\n"
    
    # Логируем в текущую сессию
    with open(LOG_SESSION_FILE, "a", encoding="utf-8") as file:
        file.write(log_entry)
    
    # Логируем в общий лог
    with open(LOG_ALL_FILE, "a", encoding="utf-8") as file:
        file.write(log_entry)

def clear_session_log():
    """Очищает лог сессии."""
    with open(LOG_SESSION_FILE, "w", encoding="utf-8") as file:
        file.write("")