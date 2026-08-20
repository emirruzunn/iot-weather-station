import csv
import json
import os

HEADERS = ["timestamp", "sensor_id", "temperature", "humidity", "pressure", "rain_intensity", "wind_speed"]

def save_to_csv(data_list, filepath):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    file_exists = os.path.isfile(filepath)
    
    with open(filepath, mode="a" if file_exists else "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=HEADERS)
        if not file_exists:
            writer.writeheader()
        writer.writerows(data_list)

def save_to_json(data_list, filepath):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, mode="w", encoding="utf-8") as f:
        json.dump(data_list, f, indent=4)