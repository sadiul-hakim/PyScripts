import json

source = r"C:\Users\Sadiul Hakim\OneDrive\Desktop\Report\old_columns.json"
destination = r"C:\Users\Sadiul Hakim\OneDrive\Desktop\Report\new_columns.json"

with open(source, "r") as file:
    columns = json.load(file)

    for column in columns:
        expression: str = column['expression'].strip()

        if not expression or not expression.startswith('dataCurve'):
            continue

        expression = expression.replace(
            ")", ",5,'TIME_FILTER_MonthOverMonth_1')")

        column['expression'] = expression

    with open(destination, "w") as file:
        json.dump(columns, file, indent=4)

print("Done")
