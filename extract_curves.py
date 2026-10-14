import csv
import json
import os

path = r"C:\Users\Sadiul Hakim\OneDrive\Desktop\Curves\Wholesale\2026 DataHub-Capacity5.json"
csv_path = os.path.splitext(path)[0] + ".csv"

curves_list = []


def collect_curves(node):
    if isinstance(node, dict):
        # Capture the current curve node
        if "name" in node:
            formula = node.get("curveFormula")
            curves_list.append(
                {
                    "id": node.get("id", ""),
                    "name": node.get("name", "Unnamed"),
                    "curveFormula": formula if formula else "N/A",
                }
            )

        # Strictly recurse into the "curves" list
        for child in node.get("curves", []):
            collect_curves(child)

    elif isinstance(node, list):
        for item in node:
            collect_curves(item)


with open(path, "r", encoding="utf-8") as file:
    data = json.load(file)
    collect_curves(data)

# Export all collected curves to CSV
try:
    with open(csv_path, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["ID", "Curve Name", "Curve Formula"])
        for curve in curves_list:
            writer.writerow(
                [curve["id"], curve["name"], curve["curveFormula"]])
    print(f"Exported {len(curves_list)} curves to: {csv_path}")
except PermissionError:
    print(
        f"[ERROR] Permission denied: Please close '{csv_path}' in Excel or other programs and run the script again."
    )
