def parse_input(user_input):
    # Удаляем leading/trailing пробелы
    user_input = user_input.strip()
    
    # Проверяем на пустой ввод
    if not user_input:
        return ["Ошибка: Ввод не может быть пустым."]

    # Разбиваем ввод на части
    parts = user_input.split()
    args_list = []

    # Определяем команду
    command_parts = []
    
    for i in range(len(parts)):
        if parts[i].startswith('-') and i + 1 < len(parts):
            break  # Встречен первый аргумент
        else:
            command_parts.append(parts[i])
    
    # Если команда не найдена
    if not command_parts:
        return ["Ошибка: Команда не указана."]

    command = ' '.join(command_parts)
    args_list.append(command)  # Добавляем команду в список

    # Парсим аргументы
    for j in range(i, len(parts), 2):
        if j + 1 < len(parts) and parts[j].startswith('-'):
            arg_name = parts[j][1:]  # Убираем '-'
            arg_value = parts[j + 1]  # Следующий элемент будет значением
            args_list.append(f'{arg_name}:{arg_value}')  # Форматируем и добавляем в список
        elif parts[j].startswith('-'):
            # Обработка случая, когда аргумент указан, но нет значения
            return [f"Ошибка: Аргумент '{parts[j]}' не имеет значения."]

    return args_list
