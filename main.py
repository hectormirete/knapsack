import csv
import os
from config import MAX_VOLUME, MAX_WEIGHT


def read_knapsack_items(file_path):
    items = {}
    with open(file_path, mode="r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            item_id = int(row["id"])
            items[item_id] = {
                "name": row["name"],
                "weight": float(row["weight_kg"]),
                "volume": float(row["volume_L"]),
                "value": float(row["value"]),
                "positive_combo_id": int(row["positive_combo_id"]),
                "positive_combo_multiplier": float(row["positive_combo_multiplier"]),
                "negative_combo_id": int(row["negative_combo_id"]),
                "negative_combo_multiplier": float(row["negative_combo_multiplier"]),
            }
    return items

def read_sack(file_path):
    with open(file_path, mode="r") as file:
        return [int(line.strip().strip(",")) for line in file]

def calculate_sack(sack, items):
    total_value = 0
    total_weight = 0
    total_volume = 0

    for item_id in sack:
        if item_id in items:
            item = items[item_id]
            value = item["value"]

            if item["positive_combo_id"] in sack:
                value *= item["positive_combo_multiplier"]

            if item["negative_combo_id"] in sack:
                value *= -item["negative_combo_multiplier"]


            total_value += value
            total_weight += item["weight"]
            total_volume += item["volume"]

    return total_value, total_weight, total_volume

def main():
    knapsack_items_path = "data/knapsack_items.csv"
    sacks_folder = "sacks/"
    results_csv_path = "results.csv"

    knapsack_items = read_knapsack_items(knapsack_items_path)
    results = []

    for sack_file in os.listdir(sacks_folder):
        sack_path = os.path.join(sacks_folder, sack_file)
        sack = read_sack(sack_path)

        total_value, total_weight, total_volume = calculate_sack(sack, knapsack_items)

        results.append({
            "name": sack_file,
            "weight": total_weight,
            "volume": total_volume,
            "value": total_value,
        })

    results.sort(key=lambda x: x["value"], reverse=True)

    print("Results:")
    for result in results:
        print(
            f"Sack Name: {result['name']}, Weight: {result['weight']}, Volume: {result['volume']}, Value: {result['value']}")

    with open(results_csv_path, mode="w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=["name", "weight", "volume", "value"])
        writer.writeheader()
        writer.writerows(results)

    print(f"Resultados guardados en {results_csv_path}")

if __name__ == "__main__":
    main()