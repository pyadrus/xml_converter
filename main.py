import csv
from bs4 import BeautifulSoup

with open("input.xml", "r", encoding="utf-8") as f:
    xml_content = f.read()

soup = BeautifulSoup(xml_content, "xml")

# Find all offer elements
offers = soup.find_all("offer")

# Create a list to store the extracted data
offer_data_list = []

for offer in offers:
    offer_data = {
        "id": offer["id"],
        "available": offer["available"],
    }

    # Extract child elements of offer
    for child in offer.children:
        if child.name is not None:  # Skip NavigableString (like whitespace)
            if child.name == "param":
                offer_data[child["name"]] = child.text
            else:
                offer_data[child.name] = child.text

    # Add the extracted data to the list
    offer_data_list.append(offer_data)

# Get all unique keys
all_keys = set().union(*(d.keys() for d in offer_data_list))

# Write data to CSV file
with open("output.csv", "w", newline="", encoding="utf-8") as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=all_keys)
    writer.writeheader()
    for offer_data in offer_data_list:
        writer.writerow(offer_data)
