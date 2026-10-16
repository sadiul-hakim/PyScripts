import json


retail = {"ADVENTRES": 6, "AESIRES": 5, "APRIRES": 306, "PRISMRES": 153, "TLIRES": 319}

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
    "TVI": 3,
}

json_keys = [
    "Generation_Revenue",
    "DU_Government_Taxes",
    "Transmission_and_System_Loss",
    "Distribution_Charges",
    "Universal_Charges",
    "Government_Taxes",
    "Early_Payment_Discount",
    "FITALLSUBTOTAL",
    "GEAALLSUBTOTAL",
]

sample_column = """
{
    "name": "",
    "description": "",
    "descriptionTitle": "",
    "label": "",
    "hideColumn": false,
    "subtotal": "average",
    "type": "FORMULA",
    "expression": " dataCurve('BusinessUnitData:BusinessUnit,[ID],Type,3,SubType,145,Key,[JSON_KEY]',26,5,'TIME_FILTER_MonthOverMonth_1')",
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
"""


res_path = r"C:\Users\Sadiul Hakim\OneDrive\Desktop\res.json"


def generate_column(obj, json_key, name_list):

    list = []
    for key, value in obj.items():
        col = json.loads(sample_column)
        col["name"] = json_key + "_" + key
        col["label"] = json_key + "_" + key
        expression: str = col["expression"]
        expression = expression.replace("[ID]", str(value))
        expression = expression.replace("[JSON_KEY]", json_key)
        col["expression"] = expression

        name_list.append("DATASET__TABLE_DATA__" + col["name"])
        list.append(col)

    return list


def generate_list_column(name, list):
    col = json.loads(sample_column)
    col["name"] = name
    col["label"] = name
    col["expression"] = " + ".join(str(i) for i in list)
    return col


def generate_key_column(key):
    col = json.loads(sample_column)
    col["name"] = key
    col["label"] = key
    expression: str = (
        f"DATASET__TABLE_DATA__{key}_Retail + DATASET__TABLE_DATA__{key}_Wholesale"
    )

    col["expression"] = expression
    return col


giant_list = []
for key in json_keys:
    retail_name_list = []
    wholesale_name_list = []

    # Actual Column List
    retail_columns = generate_column(retail, key, retail_name_list)
    wholesale_columns = generate_column(wholesale, key, wholesale_name_list)

    retail_total_column = generate_list_column(f"{key}_Retail", retail_name_list)
    wholesale_total_column = generate_list_column(
        f"{key}_Wholesale", wholesale_name_list
    )

    key_column = generate_key_column(key)

    giant_list.extend(retail_columns)
    giant_list.extend(wholesale_columns)
    giant_list.append(retail_total_column)
    giant_list.append(wholesale_total_column)
    giant_list.append(key_column)


print(len(giant_list))
with open(res_path, "w") as file:
    json.dump(giant_list, file)
