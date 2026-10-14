import json

column_format = '''
{
    "name": "",
    "externalName": "",
    "externalFormat": "",
    "value": "",
    "spotProduct": "",
    "specialFields": [],
    "specialValues": [],
    "itemList": [],
    "graphicalDevice": "",
    "sectionOrder": 1,
    "startsWith": false,
    "valueOffset": 0,
    "dataType": "",
    "replaceWithExternalName": false,
    "sourceTimeZone": "",
    "targetTimeZone": "",
    "editorField": 0,
    "periodOffset": 0,
    "columnType": 4,
    "filterType": 1,
    "unique": false,
    "getNodeById": false,
    "jsonKey": "",
    "formulaText": "",
    "specialColumn": false,
    "virtualColumn": false,
    "valueRegex": "",
    "mergeColumn": "",
    "defineMissingArguments": false,
    "ignoreZeroFormulaResult": false,
    "fileOperationType": 1,
    "autoCreate": false,
    "autoCreateSystemObjectData": false
}
'''

source_path = r"C:\Users\Sadiul Hakim\OneDrive\Desktop\Importer\Source.json"
result_path = r"C:\Users\Sadiul Hakim\OneDrive\Desktop\Importer\Result.json"

column_list = []
with open(source_path, "r") as file:
    source = json.load(file)
    nonTimeSeriesData = source['nonTimeSeriesData'][0]
    columnFormats = nonTimeSeriesData['columnFormats']
    for cformat in columnFormats:
        if cformat['name'] == 'name':
            continue

        fmt = json.loads(column_format)
        fmt['name'] = cformat['name']
        fmt['jsonKey'] = cformat['name']
        fmt['externalName'] = cformat['externalName']
        fmt['value'] = cformat['value']
        column_list.append(fmt)

with open(result_path, "w") as file:
    json.dump(column_list, file, indent=4)
