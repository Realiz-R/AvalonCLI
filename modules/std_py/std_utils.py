from os import getcwd
init_path = getcwd()

def ip_query(ip_address):
    import requests
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

    calculator = ctypes.CDLL(init_path + r'/modules/std_lib/calculator.so')

    calculator.calculate.restype = ctypes.c_double
    calculator.calculate.argtypes = [ctypes.c_char_p]

    try:
        result = calculator.calculate(expression.encode('utf-8'))
        print(f'Результат: {result}')
    except Exception as e:
        print(f'Ошибка при вычислении: {str(e)}')

def wiki(content):
    from wikipedia import summary, set_lang
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
    import ctypes
    import os

    # Загружаем динамическую библиотеку
    lib = ctypes.CDLL(init_path + r"\modules\std_lib\get_current_directory.so")

    # Определение аргументов и возвращаемого значения функции
    buffer = ctypes.create_string_buffer(1024)  # Буфер для пути
    lib.get_current_directory.argtypes = [ctypes.c_char_p, ctypes.c_size_t]
    lib.get_current_directory.restype = ctypes.c_char_p

    # Вызов функции
    result = lib.get_current_directory(buffer, len(buffer))
    if result:
        print(f"Текущая директория: {result.decode()}")
    else:
        print("Не удалось получить текущую директорию.")
            
def cd(new_path):
    import ctypes
    import os

    # Загружаем динамическую библиотеку
    lib = ctypes.CDLL(init_path + r'/modules/std_lib/change_directory.so')

    # Определяем аргументы для change_directory
    lib.change_directory.argtypes = [ctypes.c_char_p]
    lib.change_directory.restype = ctypes.c_int

    # Изменяем директорию
    if lib.change_directory(new_path.encode('utf-8')) == 0:
        print(f"Директория успешно изменена на: {new_path}")
    else:
        print("Не удалось изменить директорию на:", new_path)

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
    import ctypes

    # Загружаем динамическую библиотеку
    lib_path = init_path + r'/modules/std_lib/touch.so'  # Убедитесь, что путь к библиотеке правильный
    lib = ctypes.CDLL(lib_path)

    # Определяем функцию для передачи строковых аргументов
    lib.touch_from_python.argtypes = [ctypes.c_char_p]  # Указываем, что функция ожидает строку (char*)
    lib.touch_from_python.restype = None  # Указываем, что функция ничего не возвращает

    lib.touch_from_python(filepath.encode('utf-8'))


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
    import requests
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
    import ctypes

    # Укажите полный путь к вашей библиотеке
    lib_path = init_path + r'/modules/std_lib/mkdir.so'
    lib = ctypes.CDLL(lib_path)

    # Определяем функцию, которую мы хотим использовать
    lib.create_from_python.argtypes = [ctypes.c_char_p]
    lib.create_from_python.restype = None

    lib.create_from_python(dir_path.encode('utf-8'))
def delete(path):
    import ctypes
    # Загружаем динамическую библиотеку
    lib_path = init_path + r'/modules/std_lib/delete.so'  # Убедитесь, что путь к библиотеке правильный
    lib = ctypes.CDLL(lib_path)

    # Определяем функцию, которую мы хотим использовать
    lib.delete_from_python.argtypes = [ctypes.c_char_p]
    lib.delete_from_python.restype = None
    lib.delete_from_python(path.encode('utf-8'))
    
import threading
import socket

def scan_port(ip, port, open_ports):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.1)
        result = sock.connect_ex((ip, port))
        if result == 0:
            open_ports.append(port)
        sock.close()
    except Exception as e:
        print(f"Ошибка при сканировании порта {port}: {e}")

def portscan(ip, start_port=1, end_port=1024):
    open_ports = []
    threads = []
    for port in range(start_port, end_port + 1):
        thread = threading.Thread(target=scan_port, args=(ip, port, open_ports))
        threads.append(thread)
        thread.start()
    for thread in threads:
        thread.join()
    return open_ports

from platform import system, version, release, processor, architecture
from os import cpu_count
from subprocess import check_output
from datetime import datetime, timedelta
import time
import GPUtil

def get_memory_info():
    """Получить информацию об оперативной памяти."""
    try:
        # Для Linux
        if system() == "Linux":
            with open("/proc/meminfo", "r") as f:
                mem_info = f.readlines()
            total_memory = int(mem_info[0].split()[1]) // 1024  # В МБ
            free_memory = int(mem_info[1].split()[1]) // 1024   # В МБ
            return total_memory, free_memory
        # Для Windows
        elif system() == "Windows":
            output = check_output(["wmic", "OS", "get", "TotalVisibleMemorySize,FreePhysicalMemory"]).decode()
            lines = output.strip().split("\n")
            total_memory = int(lines[1].split()[0]) // 1024  # В МБ
            free_memory = int(lines[1].split()[1]) // 1024   # В МБ
            return total_memory, free_memory
        # Для macOS
        elif system() == "Darwin":
            output = check_output(["vm_stat"]).decode()
            lines = output.strip().split("\n")
            page_size = int(check_output(["pagesize"]).decode().strip())
            free_memory = int(lines[1].split()[-1].rstrip(".")) * page_size // (1024 ** 2)  # В МБ
            total_memory = int(check_output(["sysctl", "-n", "hw.memsize"]).decode().strip()) // (1024 ** 2)  # В МБ
            return total_memory, free_memory
        else:
            return None, None
    except Exception as e:
        print(f"Ошибка при получении информации о памяти: {e}")
        return None, None

def get_disk_usage():
    """Получить информацию о дисковом пространстве."""
    try:
        # Для Linux и macOS
        if system() in ["Linux", "Darwin"]:
            output = check_output(["df", "-h", "/"]).decode()
            lines = output.strip().split("\n")
            usage = lines[1].split()
            total = usage[1]
            used = usage[2]
            free = usage[3]
            return total, used, free
        # Для Windows
        elif system() == "Windows":
            output = check_output(["wmic", "logicaldisk", "get", "size,freespace"]).decode()
            lines = output.strip().split("\n")
            total = int(lines[1].split()[0]) // (1024 ** 3)  # В ГБ
            free = int(lines[1].split()[1]) // (1024 ** 3)   # В ГБ
            used = total - free
            return f"{total} GB", f"{used} GB", f"{free} GB"
        else:
            return None, None, None
    except Exception as e:
        print(f"Ошибка при получении информации о диске: {e}")
        return None, None, None

def get_boot_time():
    """Получить время загрузки системы."""
    try:
        # Для Linux
        if system() == "Linux":
            with open("/proc/uptime", "r") as f:
                uptime_seconds = float(f.readline().split()[0])
            boot_time = datetime.now() - timedelta(seconds=uptime_seconds)
            return boot_time
        # Для Windows
        elif system() == "Windows":
            output = check_output(["wmic", "os", "get", "lastbootuptime"]).decode()
            boot_time_str = output.strip().split("\n")[1].split(".")[0]
            boot_time = datetime.strptime(boot_time_str, "%Y%m%d%H%M%S")
            return boot_time
        # Для macOS
        elif system() == "Darwin":
            output = check_output(["sysctl", "-n", "kern.boottime"]).decode()
            boot_time_str = output.strip().split(",")[0].split("=")[1].strip()
            boot_time = datetime.fromtimestamp(int(boot_time_str))
            return boot_time
        else:
            return None
    except Exception as e:
        print(f"Ошибка при получении времени загрузки: {e}")
        return None

def get_cpu_load():
    """Получить загрузку CPU."""
    try:
        # Для Linux и macOS
        if system() in ["Linux", "Darwin"]:
            from os import getloadavg
            load_avg = getloadavg()
            return f"Загрузка CPU: {load_avg[0]:.2f}% (1 мин), {load_avg[1]:.2f}% (5 мин), {load_avg[2]:.2f}% (15 мин)"
        # Для Windows
        elif system() == "Windows":
            output = check_output(["wmic", "cpu", "get", "loadpercentage"]).decode()
            load = output.strip().split("\n")[1].strip()
            return f"Загрузка CPU: {load}%"
        else:
            return "Загрузка CPU: Информация недоступна."
    except Exception as e:
        return f"Ошибка при получении загрузки CPU: {e}"

def gc():
    """Общая команда для проверки системы: ОС, CPU, память, диск, видеокарта и другие характеристики."""
    # Информация об операционной системе
    os_info = f"""
    === Операционная система ===
    Система: {system()}
    Версия: {version()}
    Релиз: {release()}
    Архитектура: {architecture()[0]}
    """
    
    # Информация о процессоре
    if system() == "Windows":
        cpu_info = f"""
    === Процессор ===
    Модель: {processor()}
    Логические ядра: {cpu_count()}
    {get_cpu_load()}
    """
    else:
        cpu_info = f"""
    === Процессор ===
    Модель: {processor()}
    Физические ядра: {cpu_count(logical=False)}
    Логические ядра: {cpu_count(logical=True)}
    {get_cpu_load()}
    """
    
    # Информация о памяти
    total_memory, free_memory = get_memory_info()
    if total_memory and free_memory:
        memory_info = f"""
    === Оперативная память ===
    Всего: {total_memory} MB
    Свободно: {free_memory} MB
    Используется: {total_memory - free_memory} MB
    """
    else:
        memory_info = "\n=== Оперативная память ===\nИнформация недоступна."
    
    # Информация о диске
    total_disk, used_disk, free_disk = get_disk_usage()
    if total_disk and used_disk and free_disk:
        disk_info = f"""
    === Дисковое пространство ===
    Всего: {total_disk}
    Используется: {used_disk}
    Свободно: {free_disk}
    """
    else:
        disk_info = "\n=== Дисковое пространство ===\nИнформация недоступна."
    
    # Информация о видеокарте
    gpus = GPUtil.getGPUs()
    gpu_info = "\n=== Видеокарта ==="
    if gpus:
        for gpu in gpus:
            gpu_info += f"""
    Модель: {gpu.name}
    Загрузка GPU: {gpu.load * 100}%
    Используется памяти: {gpu.memoryUsed} MB
    Всего памяти: {gpu.memoryTotal} MB
    Температура: {gpu.temperature}°C
    """
    else:
        gpu_info += "\nВидеокарта не обнаружена."
    
    # Информация о загрузке системы
    boot_time = get_boot_time()
    if boot_time:
        uptime_info = f"""
    === Время работы системы ===
    Время загрузки: {boot_time.strftime("%Y-%m-%d %H:%M:%S")}
    Время работы: {str(timedelta(seconds=int(time.time() - boot_time.timestamp())))}
    """
    else:
        uptime_info = "\n=== Время работы системы ===\nИнформация недоступна."
    
    # Общий вывод
    result = os_info + cpu_info + memory_info + disk_info + gpu_info + uptime_info
    return result
def translator(text, lang):
    import ctypes
    import os

    # Путь к DLL
    dll_path = os.path.abspath(getcwd() + "/modules/std_lib/TranslatorLib.dll")

    # Загрузка DLL
    translator_lib = ctypes.cdll.LoadLibrary(dll_path)

    # Указываем типы аргументов и возвращаемого значения
    translator_lib.Translate.argtypes = [ctypes.c_char_p, ctypes.c_char_p]
    translator_lib.Translate.restype = ctypes.c_char_p

    # Вызов функции
    result = translator_lib.Translate(text.encode("utf-8"), lang.encode("utf-8"))

    # Декодирование результата
    print(result.decode("utf-8"))