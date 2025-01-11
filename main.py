from modules.std_py import Parser
from os import system
from modules.std_py import std

print("AvalonCLI [1.0.001]")

system("chcp 65001")
system("cls")

def display_help():
    print("""
╔══════════════════════════════════════════════════════════╗
║                       HELP MENU                          ║
╠══════════════════════════════════════════════════════════╣
║ 1. calc      - Запустить калькулятор                     ║
║    Пример: calc 1 + 1                                    ║
║                                                          ║
║ 2. ipcheck   - Проверить информацию об IP-адресе         ║
║    Пример: ipcheck 8.8.8.8                               ║
║                                                          ║
║ 3. ai        - Отправить текст в нейросеть               ║
║    Пример: ai Какова погода сегодня?                     ║
║                                                          ║
║ 4. wiki      - Получить краткое содержание статьи из     ║
║    Википедии                                             ║
║    Пример: wiki Python                                   ║
║                                                          ║
║ 5. pwd       - Вывести текущую рабочую директорию        ║
║                                                          ║
║ 6. cd        - Сменить текущую директорию                ║
║    Пример: cd C:/Users                                   ║
║                                                          ║
║ 7. ps        - Вывести список текущих процессов          ║
║                                                          ║
║ 8. cls       - Очистить экран терминала                  ║
║                                                          ║
║ 9. kill      - Завершить процесс по ID                   ║
║    Пример: kill 1234                                     ║
║                                                          ║
║ 10. exit/q/quit - Выход из программы                     ║
║                                                          ║
║ 11. help      - Показать этот список команд              ║
║                                                          ║
║ 12. shorturl  - Сократить ссылку                         ║
║    Пример: shorturl https://example.com                  ║
║                                                          ║
║ 13. touch     - Создать пустой файл                      ║
║    Пример: touch newfile.txt                             ║
║                                                          ║
║ 14. ping      - Проверить доступность хоста              ║
║    Пример: ping google.com                               ║
║                                                          ║
║ 15. rm/del    - Удалить файл или директорию              ║
║    Пример: rm file.txt                                   ║
║                                                          ║
║ 16. wget      - Скачать файл по URL                      ║
║    Пример: wget http://example.com/file.txt              ║
╚══════════════════════════════════════════════════════════╝
    """)

def process_command(command):
    parsed_command = Parser.parse_input(command)[0]  # Сохраним первый элемент

    if parsed_command.startswith("calc"):
        expression = parsed_command[len("calc"):].strip()
        if expression:
            try:
                std.calc(expression)
            except (SyntaxError, NameError, ZeroDivisionError) as e:
                print(f'Ошибка при вычислении: {str(e)}')
            except Exception as e:
                print(f'Ошибка: {str(e)}')
        else:
            print("Ошибка: Выражение не указано.")

    elif parsed_command.startswith("ipcheck"):
        ip_info = parsed_command[len("ipcheck"):].strip()
        if ip_info:
            try:
                std.ip_query(ip_info)
            except Exception as e:
                print(f'Ошибка при проверке IP: {str(e)}')
        else:
            print("Ошибка: Не указан IP адрес для проверки.")

    elif parsed_command.strip().lower() == "cls":
        system("cls")

    elif parsed_command.strip() == "pwd":
        std.pwd()

    elif parsed_command.strip() == "ps":
        std.processes()

    elif parsed_command.startswith("cd"):
        cd_content = parsed_command[len("cd"):].strip()
        if cd_content:
            try:

                std.cd(cd_content)
            except Exception as e:
                print(f'Ошибка при смене директории: {str(e)}')
        else:
            print("Ошибка: Не указан путь для смены директории.")

    elif parsed_command.startswith("wiki"):
        wiki_content = parsed_command[len("wiki"):].strip()
        if wiki_content:
            try:
                std.wiki(wiki_content)
            except Exception as e:
                print(f'Ошибка при получении данных из Википедии: {str(e)}')
        else:
            print("Ошибка: Не указано слово для поиска в Википедии.")

    elif parsed_command in ["exit", "q", "quit"]:
        print("Выход из программы...")
        return False

    elif parsed_command.startswith("kill"):
        pid_kill = parsed_command[len("kill"):].strip()
        if pid_kill:
            try:
                std.kill_process(pid_kill)
            except Exception as e:
                print(f'Ошибка при завершении процесса: {str(e)}')
        else:
            print("Ошибка: Не указан PID для завершения процесса.")

    elif parsed_command.startswith("shorturl"):
        shorturl_link = parsed_command[len("shorturl"):].strip()
        if shorturl_link:
            try:
                std.shorturl(shorturl_link)
            except Exception as e:
                print(f'Ошибка при сокращении ссылки: {str(e)}')
        else:
            print("Ошибка: Не указана ссылка для сокращения.")

    elif parsed_command == "help":
        display_help()
    elif parsed_command == "ls":
        std.ls()  # Вызываем функцию для отображения файлов и директорий
    elif parsed_command.startswith("touch"):
        # Логика для создания пустого файла
        filepath = parsed_command[len("touch"):].strip()
        if filepath:
            try:
                std.touch(filepath)
            except Exception as e:
                print(f'Ошибка при создании файла: {str(e)}')
    elif parsed_command.startswith("cat"):
        # Логика для вывода содержимого файла
        filepath = parsed_command[len("cat"):].strip()
        if filepath:
            try:
                std.cat(filepath)
            except Exception as e:
                print(f'Ошибка при выводе содержимого файла: {str(e)}')
        else:
            print("Ошибка: Не указан путь для создания файла.")
    elif parsed_command.startswith("ping"):
        # Логика для пинга
        host = parsed_command[len("ping"):].strip()
        if host:
            try:
                std.ping_russian(host)
            except Exception as e:
                print(f'Ошибка при выполнении команды ping: {str(e)}')
        else:
            print("Ошибка: Не указан хост для пинга.")
    elif parsed_command.startswith("rm") or parsed_command.startswith("del"):
        import os.path
        from shutil import rmtree
        # Логика для удаления файла или директории
        parts = parsed_command.split()
        if len(parts) >= 2:
            path = parts[1]
            try:
                # Проверка, является ли путь директорией
                if os.path.isdir(path):
                    rmtree(path)  # Удалить директорию и её содержимое
                    print(f"Директория '{path}' успешно удалена.")
                else:
                    os.remove(path)      # Удалить файл
                    print(f"Файл '{path}' успешно удален.")
            except Exception as e:
                print(f'Ошибка при удалении: {str(e)}')
        else:
            print("Используйте 'rm [файл/директория]' для удаления файла или директории.")
    elif parsed_command.startswith("wget"):
        # Логика для скачивания файла
        parts = parsed_command.split()
        if len(parts) >= 2:
            url = parts[1]
            dest_path = parts[2] if len(parts) > 2 else '.'  # По умолчанию используется текущая директория
            try:
                std.wget(url, dest_path)
            except Exception as e:
                print(f'Ошибка при скачивании файла: {str(e)}')
        else:
            print("Используйте: wget [URL] [путь / имя_файла назначения]")
    elif parsed_command.startswith("mkdir"):
        # Логика для создания директории
        parts = parsed_command.split()
        if len(parts) >= 2:
            dir_path = parts[1]  # Путь для создания директории
            try:
                std.mkdir(dir_path)
            except Exception as e:
                print(f'Ошибка при создании директории: {str(e)}')
        else:
            print("Используйте: mkdir [путь_для_создания_директории]")


    else:
        print("Ошибка: Неизвестная команда.")

    return True
#    venom
def main():
    while True:
        command = input("> ").strip()
        if command:
            if not process_command(command):
                break  # Если команда exit, выходим из цикла

if __name__ == "__main__":
    main()
