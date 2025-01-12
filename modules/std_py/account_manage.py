import os
import json
import hashlib
from datetime import datetime, timedelta
from modules.std_py.utils_logs import log_message, LOG_ALL_FILE, LOG_SESSION_FILE

# Константы
LOGS_DIR = "logs"  # Папка для логов
USERS_FILE = os.path.join(LOGS_DIR, "users.json")  # Путь к файлу пользователей

def hash_password(password):
    """Хеширует пароль."""
    return hashlib.sha256(password.encode()).hexdigest()

def load_users():
    """Загружает данные пользователей из файла."""
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    return {"users": []}

def save_users(data):
    """Сохраняет данные пользователей в файл."""
    with open(USERS_FILE, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)

def register(username, password, role="user"):
    """Регистрирует нового пользователя."""
    data = load_users()
    if any(user["username"] == username for user in data["users"]):
        return False, "Пользователь с таким именем уже существует."
    new_user = {
        "id": len(data["users"]) + 1,
        "username": username,
        "password": hash_password(password),
        "role": role,
        "last_login": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    data["users"].append(new_user)
    save_users(data)
    log_message(f"Зарегистрирован новый пользователь: {username}", LOG_ALL_FILE)
    log_message(f"Зарегистрирован новый пользователь: {username}", LOG_SESSION_FILE)
    return True, "Пользователь успешно зарегистрирован."

def login(username, password):
    """Авторизует пользователя."""
    data = load_users()
    for user in data["users"]:
        if user["username"] == username and user["password"] == hash_password(password):
            user["last_login"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            save_users(data)
            log_message(f"Пользователь {username} авторизовался.", LOG_ALL_FILE)
            log_message(f"Пользователь {username} авторизовался.", LOG_SESSION_FILE)
            return True, "Авторизация успешна.", user
    log_message(f"Неудачная попытка авторизации для пользователя: {username}", LOG_ALL_FILE)
    log_message(f"Неудачная попытка авторизации для пользователя: {username}", LOG_SESSION_FILE)
    return False, "Неверное имя пользователя или пароль.", None

def check_last_activity(username):
    """Проверяет, была ли активность пользователя за последние 3 дня."""
    if not os.path.exists(LOG_ALL_FILE):
        return False
    with open(LOG_ALL_FILE, "r", encoding="utf-8") as file:
        logs = file.readlines()
    user_logs = [log for log in logs if username in log]
    if not user_logs:
        return False
    last_activity = user_logs[-1].split("]")[0].strip("[")
    last_activity_date = datetime.strptime(last_activity, "%Y-%m-%d %H:%M:%S")
    return datetime.now() - last_activity_date <= timedelta(days=3)

def require_auth():
    """Требует регистрации или авторизации."""
    data = load_users()
    if not data["users"]:
        print("Нет зарегистрированных пользователей. Пожалуйста, зарегистрируйтесь.")
        while True:
            username = input("Введите имя пользователя: ").strip()
            password = input("Введите пароль: ").strip()
            success, message = register(username, password)
            print(message)
            if success:
                return username
    else:
        print("Пожалуйста, авторизуйтесь.")
        while True:
            username = input("Введите имя пользователя: ").strip()
            password = input("Введите пароль: ").strip()
            success, message, user = login(username, password)
            print(message)
            if success:
                if not check_last_activity(username):
                    print("Прошло более 3 дней с момента последней активности. Пожалуйста, авторизуйтесь снова.")
                    continue
                return username

def change_password(username, old_password, new_password):
    """Изменяет пароль пользователя."""
    data = load_users()
    for user in data["users"]:
        if user["username"] == username and user["password"] == hash_password(old_password):
            user["password"] = hash_password(new_password)
            save_users(data)
            log_message(f"Пользователь {username} изменил пароль.", LOG_ALL_FILE)
            log_message(f"Пользователь {username} изменил пароль.", LOG_SESSION_FILE)
            return True, "Пароль успешно изменен."
    return False, "Неверное имя пользователя или старый пароль."

def change_role(username, new_role):
    """Изменяет роль пользователя."""
    data = load_users()
    for user in data["users"]:
        if user["username"] == username:
            user["role"] = new_role
            save_users(data)
            log_message(f"Роль пользователя {username} изменена на {new_role}.", LOG_ALL_FILE)
            log_message(f"Роль пользователя {username} изменена на {new_role}.", LOG_SESSION_FILE)
            return True, f"Роль пользователя {username} изменена на {new_role}."
    return False, "Пользователь не найден."

def delete_user(username, password):
    """Удаляет пользователя."""
    data = load_users()
    for user in data["users"]:
        if user["username"] == username and user["password"] == hash_password(password):
            data["users"].remove(user)
            save_users(data)
            log_message(f"Пользователь {username} удален.", LOG_ALL_FILE)
            log_message(f"Пользователь {username} удален.", LOG_SESSION_FILE)
            return True, f"Пользователь {username} удален."
    return False, "Неверное имя пользователя или пароль."

def get_user_role(username):
    # Загружаем данные из файла users.json
    with open('logs/users.json', 'r') as file:
        data = json.load(file)
    
    # Ищем пользователя по username
    for user in data['users']:
        if user['username'] == username:
            return user['role']
    
    # Если пользователь не найден, возвращаем None или сообщение об ошибке
    return None