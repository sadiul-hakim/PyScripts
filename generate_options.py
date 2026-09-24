import json

keys_path = r"C:\Users\Sadiul Hakim\OneDrive\Desktop\AEI-PM-000001 Computed Billing Retail.csv"
options_path = r"C:\Users\Sadiul Hakim\OneDrive\Desktop\options.json"

options = []

with open(keys_path, 'r') as file:
    content = file.read()
    keys = content.split(",")

    for key in keys:
        cleaned_key = key.strip()
        if not cleaned_key:
            continue
        key_dic = {
            "name": cleaned_key,
            "value": cleaned_key
        }

        options.append(key_dic)

with open(options_path, "w", encoding="utf-8") as out_file:
    json.dump(options, out_file, indent=4)

print(f"Saved {len(options)} options to: {options_path}")
