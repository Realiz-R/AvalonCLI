import requests

def ip_query(ip_address):
    """Запрашивает информацию о IP-адресе и выводит ее в красивом формате."""
    try:
        # Выполняем GET-запрос к API
        response = requests.get(f"https://api.ipquery.io/{ip_address}")

        # Проверяем, успешен ли запрос
        response.raise_for_status()

        # Преобразуем ответ в JSON-формат
        data = response.json()

        # Оформляем вывод
        print("=" * 50)
        print(f"{'Данные об IP-адресе':^50}")
        print("=" * 50)

        print(f"Айпи: {data.get('ip', 'Нет информации')}")
        
        # Проверяем и выводим информацию о провайдере
        isp_info = data.get('isp', {})
        if isp_info:
            print("-" * 50)
            print(f"{'Информация о провайдере':<25}:")
            print(f"   Провайдер (ISP): {isp_info.get('isp', 'Нет информации')}")
            print(f"   Организация:     {isp_info.get('org', 'Нет информации')}")
            print(f"   ASN:            {isp_info.get('asn', 'Нет информации')}")

        # Проверяем и выводим информацию о локации
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
def ai(content):    
    from mistralai import Mistral

    api_key = ""
    model = "mistral-large-latest"

    client = Mistral(api_key=api_key)

    chat_response = client.chat.complete(
        model = model,
        messages = [
            {
                "role": "user",
                "content": content,
            },
        ]
    )

    print(chat_response.choices[0].message.content)
