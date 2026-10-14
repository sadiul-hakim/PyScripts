import json

path = r"C:\Users\Sadiul Hakim\OneDrive\Desktop\Fields.json"
columns_path = r"C:\Users\Sadiul Hakim\OneDrive\Desktop\columns.json"

column_template = '''
{
    "name": "",
    "description": "",
    "descriptionTitle": "",
    "label": "",
    "hideColumn": false,
    "subtotal": "average",
    "type": "CELL_VALUE",
    "expression": "",
    "publishDate": null,
    "endPublishDate": null,
    "operator": null,
    "curvePhase": "26",
    "convertToCumulative": false,
    "decimalPrecision": 4,
    "subtotalWithLabel": false,
    "subtotalInHeader": false,
    "subTotalPostExpression": null,
    "subtotalLabel": null,
    "subtotalUnit": null,
    "style": {
        "light": {
            "color": "#BB86FC !important"
        },
        "dark": {
            "color": "#BB86FC !important"
        }
    },
    "apiVersion": 1,
    "publishDateFilter": null,
    "defaultValue": 0,
    "curveAction": {
        "curvePhase": 0,
        "curveName": "",
        "saveCurve": false
    },
    "summaries": [],
    "staticData": null,
    "serviceConfig": null,
    "serviceId": 0,
    "publishDates": null,
    "publishDateSize": 0,
    "jsonKey": "",
    "nodeSelector": {
        "dataClass": 0,
        "leafObject": 0,
        "rootEntity": 0,
        "treeSelector": null,
        "selectedNodes": [],
        "targetLevels": [
            0
        ],
        "hideSelectors": false
    },
    "dateFormat": null,
    "publishDateSourceTimeZone": "",
    "showPublishDate": false
}
'''


def extract_non_section_fields(node):
    fields_list = []

    field = node.get("field", node)
    data = field.get("data", {})
    name = field.get("name")

    if data.get("type") != "section" and name:
        fields_list.append({
            "name": name,
            "label": data.get("label")
        })

    for sub in data.get("fields", []):
        fields_list.extend(extract_non_section_fields(sub))

    return fields_list


with open(path, "r", encoding="utf-8") as file:
    layout = json.load(file)

all_fields = []
for item in layout:
    all_fields.extend(extract_non_section_fields(item))

print(f"Total non-section fields: {len(all_fields)}")

columns = []
for f in all_fields:
    col = json.loads(column_template)
    col["name"] = f["name"]
    col["label"] = f["label"]
    col["expression"] = f"dynamicText('[ENTITY_{f['name']}]')"

    columns.append(col)

print(f"Total columns generated: {len(columns)}")

with open(columns_path, "w", encoding="utf-8") as file:
    json.dump(columns, file, indent=4)

print(f"Saved columns to {columns_path}")
