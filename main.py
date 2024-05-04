import csv
from bs4 import BeautifulSoup

with open("input.xml", "r", encoding="utf-8") as f:
    xml_content = f.read()

soup = BeautifulSoup(xml_content, "xml")

# Найти все элементы предложения
offers = soup.find_all("offer")

# Создайте список для хранения извлеченных данных.
offer_data_list = []

for offer in offers:
    offer_data = {
        "id": offer["id"],
        "available": offer["available"],
    }

    # Извлечение дочерних элементов предложения
    for child in offer.children:
        if child.name is not None:  # Пропустить NavigableString (например, пробелы)
            if child.name == "param":
                offer_data[child["name"]] = child.text
            else:
                offer_data[child.name] = child.text

    # Добавляем полученные данные в список
    offer_data_list.append(offer_data)

# Получаем все уникальные ключи
all_keys = set().union(*(d.keys() for d in offer_data_list))

# Запись данных в CSV-файл
with open("output.csv", "w", newline="", encoding="utf-8") as csvfile:
    writer = csv.DictWriter(csvfile,  # Записываем в файл
                            fieldnames=all_keys,  # Записываем все ключи
                            delimiter=';'  # Разделитель точка и запятая
                            )
    writer.writeheader()  # Записываем заголовок
    for offer_data in offer_data_list:  # Записываем данные
        writer.writerow(offer_data)  # Записываем данные



# Функция для удаления HTML-тегов из текста
def remove_html_tags(text):
    import re
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)


# Открываем файлы для чтения и записи
with open("output.csv", "r", encoding="utf-8") as infile:
    with open("output_clean.csv", "w", newline="", encoding="utf-8") as outfile:
        reader = csv.reader(infile, delimiter=";")
        writer = csv.writer(outfile, delimiter=";")

        # Обрабатываем каждую строку в файле
        for row in reader:
            cleaned_row = [remove_html_tags(cell) if isinstance(cell, str) else cell for cell in row]
            writer.writerow(cleaned_row)