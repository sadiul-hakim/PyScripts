import json
model = '''
{
    "name": "",
    "type": "BAR",
    "publishDateSourceTimeZone": "",
    "showPublishDate": false,
    "hideSeries": false,
    "decimalPrecision": 0,
    "dataSet": {
        "type": "FORMULA",
        "dateFormat": "yyyy-MM-dd HH:mm",
        "formula": ""
    },
    "serviceId": null,
    "serviceConfig": {},
    "config": {
        "name": "",
        "type": "line",
        "encode": {
            "x": "date",
            "y": ""
        },
        "symbol": "none",
        "tooltip": {
            "valueFormatter": "function (v) { return (+v).toFixed(2);}"
        },
        "datasetId": "",
        "itemStyle": {
            "color": ""
        },
        "yAxisIndex": 0
    }
}
'''

xAxis_dict = {
    "Price ($/MWh)": 0,
}

series_path = "D:\\Trash\\Series.json"
new_series_path = "D:\\Trash\\New Series.json"

with open(series_path, 'r', encoding='utf-8') as f:
    series_data = json.load(f)

    series_list = []
    for series in series_data:
        new_series = json.loads(model)
        new_series['name'] = series['name']
        new_series['showPublishDate'] = series['showPublishDate']
        new_series['decimalPrecision'] = series['decimalPrecision']
        new_series['dataSet']['formula'] = f"round({series['expression']},2)"
        new_series['config']['name'] = series['label']
        new_series['config']['encode']['y'] = series['name']
        new_series['config']['datasetId'] = series['name']
        new_series['config']['itemStyle']['color'] = series['style']['color']
        new_series['config']['yAxisIndex'] = xAxis_dict.get(
            series['style']['y-axis']['name'], 0)
        series_list.append(new_series)

    with open(new_series_path, 'a', encoding='utf-8') as new_f:
        json.dump(series_list, new_f, ensure_ascii=False)
        new_f.write('\n')
