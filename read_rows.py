import json
import re

old_path = "C:\\Users\\Sadiul Hakim\\OneDrive\\Desktop\\QR Billing Details Report Old Json.json"
new_path = "C:\\Users\\Sadiul Hakim\\OneDrive\\Desktop\\Report-2026 QR Billing Details Report Final V2.json"
new_rows = "C:\\Users\\Sadiul Hakim\\OneDrive\\Desktop\\New Rows.json"

column_structure = '''
{
    "name": "",
    "description": "",
    "descriptionTitle": "",
    "label": "",
    "hideColumn": false,
    "subtotal": "average",
    "type": "FORMULA",
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


def modify_expression(old: str):
    if not old:
        return old

    if "Computed:Deal,[DealId],Curve,DU Charges,Key," in old:
        old = old.replace("Computed:Deal,[DealId],Curve,DU Charges,Key,",
                          "ContractAccountData:Account,?,Type,3,SubType,64,Key,")

    if "Computed:Deal,[DealId],Curve," in old:
        old = old.replace("Computed:Deal,[DealId],Curve,",
                          "ContractAccountData:Account,?,Type,3,SubType,141,Key,")

    # Replace space with underscore in Key
    old = re.sub(r'Key,([^\'"]+)', lambda m: 'Key,' +
                 m.group(1).replace(' ', '_'), old)
    old = old.replace("_._", ".")

    return old


with open(old_path, "r") as file:
    report = json.load(file)
    visualization = report['visualizations'][0]
    row = visualization['rows'][0]
    series = row['series']

    rows = []
    for series in series:
        structure = json.loads(column_structure)

        structure['name'] = series['name']
        structure['label'] = series['label']
        structure['hideColumn'] = series['hideColumn']
        structure['subtotal'] = series['subtotal']
        structure['type'] = series['type']

        # Replace formula and remove space from json key
        structure['expression'] = modify_expression(series['expression'])
        structure['decimalPrecision'] = series['decimalPrecision']
        rows.append(structure)

    print(f"Writing {len(rows)} Rows")
    with open(new_rows, 'w', encoding='utf-8') as new_f:
        json.dump(rows, new_f, ensure_ascii=False)


# with open(new_path, "r") as file:
#     report = json.load(file)
#     structure = report["structure"]
#     visualization = structure['visualizations'][0]
#     row = visualization['rows'][0]
#     series = row['series']

#     print(f"new-{len(series)}")
