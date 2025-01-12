import os
import json
import hashlib
from datetime import datetime, timedelta
from modules.std_py.utils_logs import log_message, log_command_and_result, clear_session_log
from modules.std_py.account_manage import require_auth, register, login, change_password, change_role, delete_user, get_user_role
from modules.std_py import std_utils  # Добавьте этот импорт

def expand_env_vars(text):
    """
    Заменяет переменные среды в тексте на их значения.
    Пример: "$HOME" → "/home/user".
    """
    return os.path.expandvars(text)

# Константы
LOGS_DIR = "logs"  # Папка для логов
USERS_FILE = os.path.join(LOGS_DIR, "users.json")  # Путь к файлу пользователей
LOG_SESSION_FILE = os.path.join(LOGS_DIR, "log_session.txt")  # Лог текущей сессии
LOG_ALL_FILE = os.path.join(LOGS_DIR, "log_all.txt")  # Лог всей истории

# Создаем папку logs, если она не существует
if not os.path.exists(LOGS_DIR):
    os.makedirs(LOGS_DIR)

# Настройка консоли
os.system("chcp 65001")  # Устанавливаем кодировку консоли на UTF-8
os.system("cls")

print("AvalonCLI [2.1.130]")

def display_help():
    """Выводит справочное меню."""
    print("""
╔══════════════════════════════════════════════════════════╗
║                       HELP MENU                          ║
╠══════════════════════════════════════════════════════════╣
║ 1. register [user] [pass] - Зарегистрировать нового      ║
║    пользователя                                          ║
║                                                          ║
║ 2. login [user] [pass]    - Авторизоваться               ║
║                                                          ║
║ 3. changepass [old] [new] - Изменить пароль              ║
║                                                          ║
║ 4. delete_user [user] [pass] - Удалить пользователя      ║
║                                                          ║
║ 5. calc [выражение]       - Запустить калькулятор        ║
║    Пример: calc 1 + 1                                    ║
║                                                          ║
║ 6. ipcheck [IP]           - Проверить информацию об IP   ║
║    Пример: ipcheck 8.8.8.8                               ║
║                                                          ║
║ 7. cls                   - Очистить экран терминала      ║
║                                                          ║
║ 8. pwd                   - Вывести текущую директорию    ║
║                                                          ║
║ 9. cd [путь]            - Сменить директорию             ║
║    Пример: cd C:/Users                                   ║
║                                                          ║
║ 10. ps                  - Вывести список процессов       ║
║                                                          ║
║ 11. wiki [запрос]       - Поиск в Википедии              ║
║    Пример: wiki Python                                   ║
║                                                          ║
║ 12. kill [PID]          - Завершить процесс по ID        ║
║    Пример: kill 1234                                     ║
║                                                          ║
║ 13. shorturl [ссылка]   - Сократить ссылку               ║
║    Пример: shorturl https://example.com                  ║
║                                                          ║
║ 14. touch [файл]        - Создать пустой файл            ║
║    Пример: touch newfile.txt                             ║
║                                                          ║
║ 15. cat [файл]          - Вывести содержимое файла       ║
║    Пример: cat filename.txt                              ║
║                                                          ║
║ 16. ping [хост]         - Проверить доступность хоста    ║
║    Пример: ping google.com                               ║
║                                                          ║
║ 17. rm/del [путь]       - Удалить файл или директорию    ║
║    Пример: rm file.txt                                   ║
║                                                          ║
║ 18. wget [URL] [путь]   - Скачать файл по URL            ║
║    Пример: wget http://example.com/file.txt              ║
║                                                          ║
║ 19. mkdir [путь]        - Создать директорию             ║
║    Пример: mkdir new_folder                              ║
║                                                          ║
║ 20. exit/q/quit         - Выход из программы             ║
║                                                          ║
║ 21. help                - Показать этот список команд    ║
║                                                          ║
║ 22. whoami              - Показать текущего пользователя ║
║                                                          ║
║ 23. portscan [IP] (начальный_порт) (конечный_порт)       ║
║ - Сканировать открытые порты                             ║           
║    Пример: portscan 192.168.1.1 1 1000                   ║
║                                                          ║
║ 24. todo add [задача]   - Добавить задачу в список       ║
║    Пример: todo add Купить молоко                        ║
║                                                          ║
║ 25. todo list           - Показать список задач          ║
║                                                          ║
║ 26. todo remove [номер] - Удалить задачу по номеру       ║
║    Пример: todo remove 1                                 ║
║                                                          ║
╠══════════════════════════════════════════════════════════╣
║                        DEV MENU                          ║
╠══════════════════════════════════════════════════════════╣
║ 1. get_role [user]     - Показать роль пользователя      ║
║    Пример: get_role user                                 ║
║                                                          ║
║ 2. change_role [user] [role] - Изменить роль пользователя║
║    Пример: change_role user booster                      ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝
    """)

def process_command(command, username):
    command = expand_env_vars(command)
    """Обрабатывает команду и возвращает результат."""
    try:
        if command.startswith("register"):
            parts = command.split()
            if len(parts) < 3:
                raise ValueError("Используйте: register [имя пользователя] [пароль]")
            username_reg = parts[1]
            password_reg = parts[2]
            success, message = register(username_reg, password_reg)
            print(message)
            return message, username  # Возвращаем текущее имя пользователя
            
        elif command == "gc":
            result = std_utils.gc()
            print(result)
            return result, username
        
        elif command.startswith("translator"):
            parts = command.split(maxsplit=2)
            if len(parts) < 3:
                raise ValueError("Используйте: translator [язык] [текст]")
            dest_lang = parts[1]
            text = parts[2]
            translated_text = std_utils.translator(text, dest_lang)
            print(f"Перевод: {translated_text}")
            return translated_text, username

        elif command.startswith("login"):
            parts = command.split()
            if len(parts) < 3:
                raise ValueError("Используйте: login [имя пользователя] [пароль]")
            username_login = parts[1]
            password_login = parts[2]
            success, message, user = login(username_login, password_login)
            print(message)
            if success:
                return message, username_login  # Возвращаем новое имя пользователя
            return message, username  # Возвращаем текущее имя пользователя

        elif command.startswith("changepass"):
            parts = command.split()
            if len(parts) < 4:
                raise ValueError("Используйте: changepass [старый пароль] [новый пароль]")
            old_password = parts[1]
            new_password = parts[2]
            success, message = change_password(username, old_password, new_password)
            print(message)
            return message, username

        elif command.startswith("change_role"):
            from modules.std_py.account_manage import get_user_role
            # Проверяем роль текущего пользователя
            user_role = get_user_role(username)
            if user_role != "dev":
                raise ValueError("Команда доступна только для пользователей с ролью 'dev'.")
            
            parts = command.split()
            if len(parts) < 3:
                raise ValueError("Используйте: change_role [имя пользователя] [новая роль]")
            target_user = parts[1]
            new_role = parts[2]
            success, message = change_role(target_user, new_role)
            print(message)
            return message, username

        elif command.startswith("delete_user"):
            parts = command.split()
            if len(parts) < 3:
                raise ValueError("Используйте: delete_user [имя пользователя] [пароль]")
            target_user = parts[1]
            password = parts[2]
            success, message = delete_user(target_user, password)
            print(message)
            return message, username

        elif command.startswith("portscan"):
            parts = command.split()
            if len(parts) < 2:
                raise ValueError("Используйте: portscan [IP] (начальный_порт) (конечный_порт)")
            
            ip = parts[1]
            start_port = int(parts[2]) if len(parts) > 2 else 1
            end_port = int(parts[3]) if len(parts) > 3 else 1024

            if start_port < 1 or end_port > 65535 or start_port > end_port:
                raise ValueError("Некорректный диапазон портов. Допустимые значения: 1-65535.")

            print(f"Сканирование портов на {ip}...")
            open_ports = std_utils.portscan(ip, start_port, end_port)

            if open_ports:
                result = f"Открытые порты на {ip}: {', '.join(map(str, open_ports))}"
            else:
                result = f"На {ip} не найдено открытых портов в диапазоне {start_port}-{end_port}."
            
            print(result)
            return result, username

        elif command.startswith("todo"):
            parts = command.split(maxsplit=1)
            if len(parts) < 2:
                raise ValueError("Используйте: todo add [задача], todo list, todo remove [номер]")
            
            action = parts[1].split()[0]
            if action == "add":
                task = parts[1].split(maxsplit=1)[1]
                with open("logs/todo.json", "a", encoding="utf-8") as f:
                    json.dump({"task": task, "user": username}, f)
                    f.write("\n")
                result = f"Задача добавлена: {task}"
            elif action == "list":
                with open("logs/todo.json", "r", encoding="utf-8") as f:
                    tasks = [json.loads(line) for line in f]
                result = "\n".join([f"{i+1}. {task['task']} (пользователь: {task['user']})" for i, task in enumerate(tasks)])
            elif action == "remove":
                task_id = int(parts[1].split()[1]) - 1
                with open("logs/todo.json", "r", encoding="utf-8") as f:
                    tasks = [json.loads(line) for line in f]
                if 0 <= task_id < len(tasks):
                    removed_task = tasks.pop(task_id)
                    with open("logs/todo.json", "w", encoding="utf-8") as f:
                        for task in tasks:
                            json.dump(task, f)
                            f.write("\n")
                    result = f"Задача удалена: {removed_task['task']}"
                else:
                    result = "Ошибка: Неверный номер задачи."
            else:
                result = "Ошибка: Неизвестное действие."
            print(result)
            return result, username

        elif command.startswith("calc"):
            expression = command[len("calc"):].strip()
            if not expression:
                raise ValueError("Ошибка: Выражение не указано.")
            result = std_utils.calc(expression)
            print(result)
            return result, username

        elif command.startswith("ipcheck"):
            ip_info = command[len("ipcheck"):].strip()
            if not ip_info:
                raise ValueError("Ошибка: Не указан IP адрес для проверки.")
            result = std_utils.ip_query(ip_info)
            print(result)
            return result, username

        elif command.strip().lower() == "cls":
            os.system("cls")
            return "Командная строка очищена успешно.", username

        elif command.strip() == "pwd":
            result = std_utils.pwd()
            print(result)
            return result, username

        elif command.strip() == "ps":
            result = std_utils.processes()
            print(result)
            return result, username

        elif command.startswith("cd"):
            cd_content = command[len("cd"):].strip()
            if not cd_content:
                raise ValueError("Ошибка: Не указан путь для смены директории.")
            result = std_utils.cd(cd_content)
            print(result)
            return result, username

        elif command.startswith("wiki"):
            wiki_content = command[len("wiki"):].strip()
            if not wiki_content:
                raise ValueError("Ошибка: Не указано слово для поиска в Википедии.")
            result = std_utils.wiki(wiki_content)
            print(result)
            return result, username

        elif command in ["exit", "q", "quit"]:
            print("Выход из программы...")
            clear_session_log()
            return "exit", username

        elif command.startswith("kill"):
            pid_kill = command[len("kill"):].strip()
            if not pid_kill:
                raise ValueError("Ошибка: Не указан PID для завершения процесса.")
            result = std_utils.kill_process(pid_kill)
            print(result)
            return result, username

        elif command.startswith("shorturl"):
            shorturl_link = command[len("shorturl"):].strip()
            if not shorturl_link:
                raise ValueError("Ошибка: Не указана ссылка для сокращения.")
            result = std_utils.shorturl(shorturl_link)
            print(result)
            return result, username

        elif command == "help":
            display_help()
            return "Справка отображена успешно.", username

        elif command == "ls":
            result = std_utils.ls()
            print(result)
            return result, username

        elif command.startswith("touch"):
            filepath = command[len("touch"):].strip()
            if not filepath:
                raise ValueError("Ошибка: Не указан путь для создания файла.")
            result = std_utils.touch(filepath)
            print(result)
            return result, username

        elif command.startswith("cat"):
            filepath = command[len("cat"):].strip()
            if not filepath:
                raise ValueError("Ошибка: Не указан путь для вывода содержимого файла.")
            result = std_utils.cat(filepath)
            print(result)
            return result, username

        elif command.startswith("ping"):
            host = command[len("ping"):].strip()
            if not host:
                raise ValueError("Ошибка: Не указан хост для пинга.")
            result = std_utils.ping_russian(host)
            print(result)
            return result, username

        elif command.startswith("rm") or command.startswith("del"):
            parts = command.split()
            if len(parts) < 2:
                raise ValueError("Используйте 'rm [файл/директория]' для удаления файла или директории.")
            path = parts[1]
            if os.path.isfile(path):
                os.remove(path)
                result = f"Файл {path} удален."
            elif os.path.isdir(path):
                os.rmdir(path)
                result = f"Директория {path} удалена."
            else:
                result = f"Ошибка: {path} не найден."
            print(result)
            return result, username

        elif command.startswith("wget"):
            parts = command.split()
            if len(parts) < 2:
                raise ValueError("Используйте: wget [URL] [путь / имя_файла назначения]")
            url = parts[1]
            dest_path = parts[2] if len(parts) > 2 else '.'  # По умолчанию используется текущая директория
            result = std_utils.wget(url, dest_path)
            print(result)
            return result, username

        elif command.startswith("mkdir"):
            parts = command.split()
            if len(parts) < 2:
                raise ValueError("Используйте: mkdir [путь_для_создания_директории]")
            dir_path = parts[1]  # Путь для создания директории
            result = std_utils.mkdir(dir_path)
            print(result)
            return result, username

        elif command == "whoami":
            result = f"Текущий пользователь: {username}"
            print(result)
            return result, username

        elif command.startswith("get_role"):
            # Проверяем роль текущего пользователя
            user_role = get_user_role(username)
            if user_role != "dev":
                raise ValueError("Команда доступна только для пользователей с ролью 'dev'.")
            
            parts = command.split()
            if len(parts) < 2:
                raise ValueError("Используйте: get_role [имя пользователя]")
            target_user = parts[1]
            role = get_user_role(target_user)
            if role:
                result = f"Роль пользователя {target_user}: {role}"
            else:
                result = f"Пользователь {target_user} не найден."
            print(result)
            return result, username

        else:
            raise ValueError("Ошибка: Неизвестная команда.")

    except Exception as e:
        error_msg = f"Ошибка: {str(e)}"
        print(error_msg)
        return error_msg, username  # Возвращаем сообщение об ошибке и текущее имя пользователя

def main():
    """Основной цикл программы."""
    username = require_auth()  # Требуем регистрации или авторизации
    while True:
        command = input("> ").strip()
        if command:
            result, username = process_command(command, username)  # Обновляем username
            log_command_and_result(command, result, username)  # Логируем с именем пользователя
            if result == "exit":
                break

if __name__ == "__main__":
    try:
        main()
    finally:
        clear_session_log()  # Очищаем лог сессии при завершении программы