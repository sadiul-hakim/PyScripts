import json


retail = {
    "ADVENTRES": 6,
    "AESIRES": 5,
    "APRIRES": 306,
    "PRISMRES": 153,
    "TLIRES": 319
}

wholesale = {
    "APRI": 84,
    "ASPI": 334,
    "CPPC": 101,
    "EAUC": 102,
    "HBI": 181,
    "HI": 18,
    "HSAB": 321,
    "HSI": 286,
    "HTI": 311,
    "PEC": 4,
    "PVSI": 331,
    "RERI": 333,
    "SACASUN": 121,
    "TLI": 2,
    "TMI": 180,
    "TMO": 69,
    "TPVI": 109,
    "TSI": 179,
    "TVI": 3
}

sample_column = '''
{
    "name": "",
    "description": "",
    "descriptionTitle": "",
    "label": "",
    "hideColumn": false,
    "subtotal": "average",
    "type": "FORMULA",
    "expression": " dataCurve('BusinessUnitData:BusinessUnit,[ID],Type,3,SubType,145,Key,[JSON_KEY]',26)",
    "publishDate": null,
    "endPublishDate": null,
    "operator": null,
    "curvePhase": "16",
    "convertToCumulative": false,
    "decimalPrecision": 2,
    "subtotalWithLabel": false,
    "subtotalInHeader": false,
    "subTotalPostExpression": null,
    "subtotalLabel": null,
    "subtotalUnit": null,
    "style": {
        "light": {
            "color": "#0288D1 !important"
        },
        "dark": {
            "color": "#0288D1 !important"
        },
        "commaSeparated": true
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
    "publishDateSourceTimeZone": null,
    "showPublishDate": false
}
'''

JSON_KEY_KWH = "kWh_Billed"
JSON_KEY_TOTAL_BILL = "Total_Bill"

res_path = r"C:\Users\Sadiul Hakim\OneDrive\Desktop\res.json"

retail_total_column_name = []
retail_kwh_column_name = []
wholesale_total_column_name = []
wholesale_kwh_column_name = []


def generate_column(obj, json_key, name_list):

    list = []
    for key, value in obj.items():
        col = json.loads(sample_column)
        col['name'] = json_key + "_" + key
        col['label'] = json_key + "_" + key
        expression: str = col['expression']
        expression = expression.replace('[ID]', str(value))
        expression = expression.replace('[JSON_KEY]', json_key)
        col['expression'] = expression

        name_list.append("DATASET__TABLE_DATA__"+col['name'])
        list.append(col)

    return list


def generate_list_column(name, list):
    col = json.loads(sample_column)
    col['name'] = name
    col['label'] = name

    expression = ''
    for i in list:
        expression += f"{i} + "

    col['expression'] = expression
    return col


retail_total_columns = generate_column(
    retail, JSON_KEY_TOTAL_BILL, retail_total_column_name)
retail_kwh_columns = generate_column(
    retail, JSON_KEY_KWH, retail_kwh_column_name)


wholesale_total_columns = generate_column(
    wholesale, JSON_KEY_TOTAL_BILL, wholesale_total_column_name)
wholesale_kwh_columns = generate_column(
    wholesale, JSON_KEY_KWH, wholesale_kwh_column_name)

# totals

kWh_Billed_Retail = generate_list_column(
    'kWh_Billed_Retail', retail_kwh_column_name)
Total_Bill_Wholesale = generate_list_column(
    'Total_Bill_Retail', retail_total_column_name)

kWh_Billed_Wholesale = generate_list_column(
    'kWh_Billed_Wholesale', wholesale_kwh_column_name)
Total_Bill_Retail = generate_list_column(
    'Total_Bill_Wholesale', wholesale_total_column_name)

giant_list = retail_total_columns + retail_kwh_columns + \
    wholesale_total_columns + wholesale_kwh_columns

giant_list.append(kWh_Billed_Retail)
giant_list.append(Total_Bill_Wholesale)
giant_list.append(kWh_Billed_Wholesale)
giant_list.append(Total_Bill_Retail)

print(len(giant_list))
with open(res_path, "w") as file:
    json.dump(giant_list, file)
