import csv
from bs4 import BeautifulSoup
from loguru import logger

# Словарь для соответствия идентификатора категории и ее текстового представления
category_mapping = {
    "1": "Электроочаги",
    "29": "Электроочаги (2D электроочаги)",
    "31": "Электроочаги (3D электроочаги)",
    "35": "Электроочаги (Встраиваемые очаги)",
    "34": "Электроочаги (Классические очаги)",
    "30": "Электроочаги (Линейные очаги)",
    "37": "Электроочаги (Широкие очаги)",
    "2": "Порталы для электрокаминов",
    "32": "Порталы для электрокаминов (Деревянные порталы)",
    "33": "Порталы для электрокаминов (Каменные порталы)",
    "42": "Порталы для электрокаминов (Линейные порталы)",
    "43": "Порталы для электрокаминов (Угловые порталы)",
    "553": "Порталы для электрокаминов (Пристенные порталы)",
    "533": "Электрокамины",
    "534": "Электрокамины (Деревянные электрокамины)",
    "535": "Электрокамины (Электрокамины под камень)",
    "536": "Электрокамины (Линейные электрокамины)",
    "537": "Электрокамины (Угловые электрокамины)",
    "543": "Электрокамины (3D Электрокамины)",
    "541": "Электрокамины (Кантри)",
    "539": "Электрокамины (Классические)",
    "568": "Электрокамины (Маленькие электрокамины)",
    "592": "Электрокамины (Настенные)",
    "542": "Электрокамины (Паровые камины)",
    "540": "Электрокамины (Современные)"
}

with open("input.xml", "r", encoding="utf-8") as f:
    xml_content = f.read()

soup = BeautifulSoup(xml_content, "xml")

offers = soup.find_all("offer")  # Найти все элементы предложения

offer_data_list = []  # Создайте список для хранения извлеченных данных.

for offer in offers:
    offer_data = {
        "id": offer["id"],
        "available": offer["available"],
    }

    for child in offer.children:  # Извлечение дочерних элементов предложения
        if child.name is not None:  # Пропустить NavigableString (например, пробелы)
            if child.name == "param":
                offer_data[child["name"]] = child.text
            else:
                offer_data[child.name] = child.text

    offer_data_list.append(offer_data)  # Добавляем полученные данные в список

logger.debug(offer_data_list)
all_keys = set().union(*(d.keys() for d in offer_data_list))  # Получаем все уникальные ключи

with open("output.csv", "w", newline="", encoding="utf-8") as csvfile:  # Запись данных в CSV-файл
    writer = csv.DictWriter(csvfile,  # Записываем в файл
                            fieldnames=all_keys,  # Записываем все ключи
                            delimiter=';'  # Разделитель точка и запятая
                            )
    writer.writeheader()  # Записываем заголовок
    for offer_data in offer_data_list:  # Записываем данные
        if 'categoryId' in offer_data:  # Модифицируем значение categoryId
            category_id = offer_data['categoryId']
            if category_id in category_mapping:
                offer_data['categoryId'] = category_mapping[category_id]
        writer.writerow(offer_data)  # Записываем данные


def remove_html_tags(text):  # Функция для удаления HTML-тегов из текста
    import re
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)


with open("output.csv", "r", encoding="utf-8") as infile:  # Открываем файлы для чтения и записи
    with open("output_clean.csv", "w", newline="", encoding="utf-8") as outfile:
        reader = csv.reader(infile, delimiter=";")
        writer = csv.writer(outfile, delimiter=";")

        for row in reader:  # Обрабатываем каждую строку в файле
            cleaned_row = [remove_html_tags(cell) if isinstance(cell, str) else cell for cell in row]
            writer.writerow(cleaned_row)
