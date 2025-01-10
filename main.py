from libraries import Parser
from os import system
from modules.std import std

def main():
    while True:
        command = input("> ").strip()
        if not command:
            continue  # Пропустить пустой ввод
        parsed_command = Parser.parse_input(command)[0]  # Сохраним первый элемент

        if "calc" in parsed_command:
            expression = parsed_command.replace('calc ', '').strip()  # Убираем "calc "
            try:
                if not expression:
                    raise ValueError("Ошибка: Выражение не указано.")
                # Используем безопасное выполнение арифметических выражений
                result = eval(expression, {"__builtins__": None}, {})
                print(f'Результат: {result}')
            except SyntaxError:
                print('Ошибка: Неверный синтаксис выражения.')
            except NameError:
                print('Ошибка: Использованы неразрешенные имена.')
            except ZeroDivisionError:
                print('Ошибка: Деление на ноль.')
            except Exception as e:
                print(f'Ошибка при вычислении: {str(e)}')

        elif parsed_command in ["exit", "q", "quit"]:
            print("Выход из программы...")
            break

        elif "ipcheck" in parsed_command:
            ip_info = parsed_command.replace("ipcheck ", "").strip()
            if not ip_info:
                print("Ошибка: Не указан IP адрес для проверки.")
            else:
                std.ip_query(ip_info)  # Вызов функции ip_query для проверки IP
        elif parsed_command == "cls":
            system("cls")
        elif "ai" in parsed_command:
            ai_content = parsed_command.replace("ai ", "").strip()
            std.ai(ai_content)  # Вызов функции ip_query для проверки IP
        else:
            print("Ошибка: Не удалось распознать команду!")

main()


# ехал venom через реку venom видит веном в реке venom сунул venom руку в venom venom venom venom venom venom venom venomvenom venom venom venomvenom venom venom venomvenom venom venom venomvenom venom venom venomvenom venom venom venomvenom venom venom venomvenom venom venom venom
