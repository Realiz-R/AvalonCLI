import requests
from os import getcwd, chdir
from wikipedia import summary, set_lang

def ip_query(ip_address):
    """Запрашивает информацию о IP-адресе и выводит ее в красивом формате."""
    if not ip_address:
        print("Ошибка: IP-адрес не указан.")
        return

    try:
        response = requests.get(f"https://api.ipquery.io/{ip_address}")
        response.raise_for_status()
        data = response.json()

        print("=" * 50)
        print(f"{'Данные об IP-адресе':^50}")
        print("=" * 50)
        print(f"Айпи: {data.get('ip', 'Нет информации')}")
        
        isp_info = data.get('isp', {})
        if isp_info:
            print("-" * 50)
            print(f"{'Информация о провайдере':<25}:")
            print(f"   Провайдер (ISP): {isp_info.get('isp', 'Нет информации')}")
            print(f"   Организация:     {isp_info.get('org', 'Нет информации')}")
            print(f"   ASN:            {isp_info.get('asn', 'Нет информации')}")

        location_info = data.get('location', {})
        if location_info:
            print("-" * 50)
            print(f"{'Локация':<25}:")
            print(f"   Страна:           {location_info.get('country', 'Нет информации')}")
            print(f"   Код страны:       {location_info.get('country_code', 'Нет информации')}")
            print(f"   Город:           {location_info.get('city', 'Нет информации')}")
            print(f"   Штат:            {location_info.get('state', 'Нет информации')}")
            print(f"   Почтовый индекс: {location_info.get('zipcode', 'Нет информации')}")
            print(f"   Широта:         {location_info.get('latitude', 'Нет информации')}")
            print(f"   Долгота:        {location_info.get('longitude', 'Нет информации')}")
            print(f"   Часовой пояс:   {location_info.get('timezone', 'Нет информации')}")
            print(f"   Местное время:  {location_info.get('localtime', 'Нет информации')}")

        print("=" * 50)

    except requests.exceptions.RequestException as e:
        print(f"Произошла ошибка при выполнении запроса: {e}")

#def ai(content):
#    """Отправляет запрос к нейросети и выводит ответ."""
#    if not content:
#        print("Ошибка: Не указан текст для нейросети.")
#        return
#
#    api_key = "your_api_key_here"  # Используйте переменные окружения для безопасности
#    model = "mistral-large-latest"
#
#    client = Mistral(api_key=api_key)
#
#    try:
#        chat_response = client.chat.complete(
#            model=model,
#            messages=[
#               {
#                    "role": "user",
#                    "content": content,
#                },
#            ]
#        )
#
#        print(chat_response.choices[0].message.content)
#    except Exception as e:
#        print(f"Ошибка при запросе к нейросети: {e}")

def calc(expression):
    """Вычисляет математическое выражение с помощью внешней библиотеки."""
    import ctypes

    if not expression:
        print("Ошибка: Выражение не указано.")
        return

    calculator = ctypes.CDLL('./modules/std_lib/calculator.so')

    calculator.calculate.restype = ctypes.c_double
    calculator.calculate.argtypes = [ctypes.c_char_p]

    try:
        result = calculator.calculate(expression.encode('utf-8'))
        print(f'Результат: {result}')
    except Exception as e:
        print(f'Ошибка при вычислении: {str(e)}')

def wiki(content):
    """Получает краткое содержание статьи из Википедии."""
    if not content:
        print("Ошибка: Не указано слово для поиска в Википедии.")
        return

    set_lang("ru")
    try:
        result = summary(content)
        print(result)
    except Exception as e:
        print(f'Ошибка при получении данных из Википедии: {str(e)}')

def pwd():
    """Выводит текущую рабочую директорию."""
    print(getcwd())

def cd(content):
    """Сменяет текущую директорию на указанную."""
    if not content:
        print("Ошибка: Не указан путь для смены директории.")
        return

    try:
        chdir(content)
        print(f"Текущая директория: {getcwd()}")
    except Exception as e:
        print(f'Ошибка при смене директории: {str(e)}')

def processes():
    import os
    """Получает и выводит список текущих процессов."""
    for pid in os.listdir('/proc'):
        if pid.isdigit():  # Проверяем, что это число (PID)
            try:
                with open(os.path.join('/proc', pid, 'stat')) as f:
                    stat = f.read().strip().split()
                    # Получаем информацию о процессе
                    process_info = {
                        'pid': pid,
                        'name': stat[1].strip('()'),  # Имя процесса
                        'state': stat[2],  # Состояние
                        'utime': stat[13],  # Время процессорного времени в пользовательском режиме
                        'stime': stat[14],  # Время процессорного времени в системном режиме
                    }
                    # Выводим информацию о процессе
                    print(f"PID: {process_info['pid']}, Name: {process_info['name']}, "
                          f"State: {process_info['state']}, User Time: {process_info['utime']}, "
                          f"System Time: {process_info['stime']}")
            except IOError:  # Процесс может завершиться между чтениями
                continue
def processes():
    import ctypes

    # Загрузка динамической библиотеки
    process_list_lib = ctypes.CDLL('./modules/std_lib/process_list.so')

    # Вызов функции print_processes из библиотеки
    process_list_lib.print_processes()

def kill_process(pid):
    from os import name
    import subprocess
    """
    Завершает процесс по его PID, используя команду операционной системы.

    :param pid: Идентификатор процесса, который нужно завершить.
    :return: Строка с сообщением о результате операции.
    """
    try:
        # Для Windows используем taskkill, для Unix (Linux, macOS) используем kill
        if name == 'nt':  # Windows
            command = ['taskkill', '/F', '/PID', str(pid)]
        else:  # Unix
            command = ['kill', str(pid)]

        subprocess.run(command, check=True)  # Запускаем команду
        return f"Процесс {pid} был успешно завершён."
    except subprocess.CalledProcessError:
        return f"Не удалось завершить процесс {pid} (возможно, он не существует)."
    except Exception as e:
        return f"Произошла ошибка: {e}"

def shorturl(link):
    import requests
    endpoint = 'https://clck.ru/--'
    url = (link, '?utm_source=sender')
    response = requests.get(
        endpoint,
        params = {'url': url}
    )
    print(response.text)
    

def ls(path=".", prefix=""):
    import os
    """Выводит содержимое указанного каталога в виде древовидной структуры."""
    try:
        entries = os.listdir(path)
        entries.sort()  # Сортируем для упорядоченного вывода

        for index, entry in enumerate(entries):
            item_path = os.path.join(path, entry)
            is_last = index == len(entries) - 1
            
            # Форматируем вывод и добавляем префикс к элементам
            connector = "└── " if is_last else "├── "
            print(f"{prefix}{connector}{entry}")
            
            # Если это директория, рекурсивно вызываем функцию
            if os.path.isdir(item_path):
                next_prefix = prefix + ("    " if is_last else "│   ")
                ls(item_path, next_prefix)

    except FileNotFoundError:
        print(f"Указанный каталог '{path}' не найден.")
    except PermissionError:
        print(f"Нет разрешения для доступа к каталогу '{path}'.")
    except Exception as e:
        print(f"Произошла ошибка: {str(e)}")
        
def touch(filepath):
    import os
    """Создает пустой файл с указанным именем в указанном пути."""
    try:
        # Получаем директорию из пути файла
        directory = os.path.dirname(filepath) or '.'  # Используем текущую директорию, если директория не указана

        # Проверяем, существует ли директория
        if not os.path.exists(directory):
            raise FileNotFoundError(f"Директория '{directory}' не найдена.")
        
        # Создаем пустой файл или обновляем время последнего доступа/изменения
        with open(filepath, 'a'):
            os.utime(filepath, None)  # Обновляем метаданные файла, если он существует
        print(f"Файл '{filepath}' успешно создан или обновлён.")
    
    except FileNotFoundError as fnf_error:
        print(fnf_error)
    except PermissionError:
        print(f"Нет разрешения для создания файла '{filepath}'.")
    except Exception as e:
        print(f"Ошибка при создании файла '{filepath}': {e}")

def cat(filepath):
    import os
    """Выводит содержимое указанного файла в консоль."""
    try:
        if os.path.isfile(filepath):
            with open(filepath, 'r', encoding='utf-8') as f:
                contents = f.read()
                print(contents)
        else:
            print(f"Файл '{filepath}' не найден.")
    except Exception as e:
        print(f"Ошибка при чтении файла '{filepath}': {e}")
def ping_russian(host):
    import subprocess
    import re
    """Запускает команду ping и переводит вывод на русский язык с красивым форматированием."""
    
    translations = {
        "Pinging": "Пингую",
        "with 32 bytes of data:": "с 32 байтами данных:",
        "Reply from": "Ответ от",
        "bytes=": "байт=",
        "time=": "время=",
        "TTL=": "TTL=",
        "ms": "мс",
        "Packets: Sent =": "Пакетов: Отправлено =",
        "Received =": "Получено =",
        "Lost =": "Потеря =",
        "Ping statistics for": "Статистика пинга для",
        "Approximate round trip times in milli-seconds:": "Приблизительное время приема-передачи в мс:",
        "Minimum =": "Минимальное =",
        "Maximum =": "Максимальное =",
        "Average =": "Среднее =",
        "loss": "потеряно",
        "Request timed out.": "Время ожидания истекло."
    }

    try:
        result = subprocess.run(['ping', host], capture_output=True, text=True, check=True)
        output = result.stdout

        # Паттерн для замены фраз на русский
        def translate(match):
            return translations.get(match.group(0), match.group(0))  # Возвращает оригинал, если нет перевода

        # Замена фраз
        translated_output = re.sub('|'.join(map(re.escape, translations.keys())), translate, output)

        # Форматированный вывод с заголовком
        print("=" * 50)
        print(f"{'Результаты пинга':^50}")  # Заголовок по центру
        print("=" * 50)
        
        # Поделим вывод на строки для более красивого оформления
        for line in translated_output.splitlines():
            print(f"{line:<50}")  # Выравнивание по левому краю с фиксированной шириной

        print("=" * 50)

    except subprocess.CalledProcessError as e:
        print(f"Ошибка при выполнении команды ping: {e}")
    except FileNotFoundError:
        print("Команда ping не найдена.")
    
def wget(url, dest_path):
    import os
    """Скачивает файл по указанному URL и сохраняет его по указанному пути."""
    try:
        response = requests.get(url)
        response.raise_for_status()  # Проверка на ошибки состояния запроса

        # Получение имени файла из URL, если не указано имя файла
        if os.path.isdir(dest_path):
            filename = url.split("/")[-1]  # Извлечение имени файла из URL
            dest_path = os.path.join(dest_path, filename)

        # Запись содержимого ответа в файл
        with open(dest_path, 'wb') as file:
            file.write(response.content)
        print(f"Файл '{dest_path}' успешно скачан.")

    except requests.exceptions.RequestException as e:
        print(f'Ошибка при скачивании файла: {str(e)}')
    except Exception as e:
        print(f'Общая ошибка: {str(e)}')
        
def mkdir(dir_path):
    from os import makedirs
    """Создает директорию по указанному пути."""
    try:
        # Создание директории, если её ещё не существует
        makedirs(dir_path, exist_ok=True)
        print(f"Директория '{dir_path}' успешно создана.")
    except OSError as e:
        print(f'Ошибка при создании директории: {str(e)}')
    except Exception as e:
        print(f'Общая ошибка: {str(e)}')