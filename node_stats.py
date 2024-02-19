from datetime import datetime
from requests import get as rget
import sys
import json

# Dateipfad zur JSON-Datei mit dem Dictionary
file_path = "cities_to_nodes_urls.json"

# Das Dictionary aus der JSON-Datei laden
with open(file_path, "r") as file:
    cities_to_urls = json.load(file)


def scrape(url):
    '''returns remote json'''
    try:
        return rget(url, timeout=10).json()
    except Exception as ex:
        print(f"Error: {ex}")

def save_to_json(filename, data):
    try:
        with open(filename, 'w', encoding="utf8") as fn:
            json.dump(data, fn, indent=4, ensure_ascii=False)
    except OSError as ex:
        sys.exit(ex)
        


# Durch das Dictionary von Stadt/Ort und URL iterieren
for city, url in cities_to_urls.items():
    nodes = scrape(url)

    if nodes:
        ONLINE = 0
        for node in nodes['nodes']:
            if node['status']['online']:
                ONLINE += 1

        now = datetime.now().strftime('%H:%M %d.%m.%Y')
        result = {
            "online_nodes": ONLINE,
            "timestamp": now
        }
        filename = f"{city}-results.json"
        save_to_json(filename, result)