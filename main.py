# Импортируем необходимые библиотеки
import requests  # Для выполнения HTTP-запросов
from bs4 import BeautifulSoup  # Для парсинга HTML-страниц
import re  # Для работы с регулярными выражениями (очистка текста)


def parse_website(url):
    """
    Основная функция для парсинга веб-страницы.
    Извлекает данные из таблицы и сохраняет в словарь.
    """
    # Создаем словарь для хранения данных
    # (избегаем названия 'dict', так как это имя встроенного типа)
    parsed_data = {}

    try:
        # 1. Отправляем GET-запрос к целевой странице
        print("Отправка запроса к серверу...")
        response = requests.get(
            url,
            timeout=10  # Максимальное время ожидания ответа
        )

        # Проверяем, был ли запрос успешным (код 200)
        response.raise_for_status()

        # Устанавливаем правильную кодировку для русскоязычного контента
        response.encoding = "windows-1251"

        # 2. Парсим HTML-страницу с помощью BeautifulSoup
        print("Парсинг HTML-страницы...")
        # Используем lxml как парсер (быстрый и эффективный)
        page = BeautifulSoup(response.text, 'lxml')

        # 3. Находим нужную таблицу по классу 'tablegrey'
        table = page.find('table', class_='tablegrey')

        # Проверяем, найдена ли таблица
        if not table:
            raise ValueError("Таблица с классом 'tablegrey' не найдена на странице")

        # 4. Извлекаем все строки (tr) из таблицы
        rows = table.find_all('tr')

        print(f"Найдено {len(rows)} строк в таблице")

        # 5. Обрабатываем каждую строку таблицы
        for row in rows:
            # Находим ячейку заголовка (th) и ячейку данных (td)
            th = row.find('th')  # Ячейка с ключом
            td = row.find('td')  # Ячейка со значением

            # Пропускаем строку, если нет одной из ячеек
            if not th or not td:
                continue

            # Очищаем текст от лишних символов (переносы, табы) с помощью регулярного выражения
            # re.sub заменяет все вхождения шаблона на пустую строку
            # [\r\n\t]+ - ищем один или более символов \r, \n или \t
            key = re.sub(r'[\r\n\t]+', '', th.get_text()).strip()
            val = re.sub(r'[\r\n\t]+', '', td.get_text()).strip()

            # Добавляем очищенные данные в словарь
            parsed_data[key] = val
            print(f"Добавлена запись: {key} => {val}")

        # 6. Выводим результаты
        print("\nРезультаты парсинга:")
        for key, val in parsed_data.items():
            print(f"{key}: {val}")

        return parsed_data

    except requests.RequestException as e:
        # Обрабатываем ошибки, связанные с HTTP-запросом
        print(f"Ошибка при выполнении запроса: {e}")
    except Exception as e:
        # Обрабатываем все остальные возможные ошибки
        print(f"Произошла непредвиденная ошибка: {e}")
    finally:
        print("Завершение работы парсера")

# Запускаем функцию парсинга
if __name__ == "__main__":

    url='https://izgr.ru/?mod=boards&page=single&id=77223'
    data = parse_website(url)