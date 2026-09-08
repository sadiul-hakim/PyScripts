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

tab_xAxis_dict = [
    {
        "Prices ($/MWh)": 0,
        "Demand (MW)": 1,
    },
    {
        "Prices ($/MWh)": 0,
        "Demand (MW)": 1,
    },
    {
        "Weather (°F)": 0,
        "Price ($/MWh)": 1,
        "Demand (MW)": 2,
    },
    {
        "Price ($/MWh)": 0,
        "Demand (MW)": 1,
        "Renewables Generation (MW)": 2,
    },
    {
        "Price ($/MWh)": 0,
        "Demand & Generation (MW)": 1,
    },
    {
        "Price  ($/MWh)": 0,
        "Renewables by Demand (MW)": 1
    }
]

chartType = {
    'line': 'line',
    'column': 'bar',
}

tabs_path = "D:\\Trash\\Tabs.json"
new_tabs_path = "D:\\Trash\\New Tabs Series.json"

all_series = []


def convert_series(series_data, xAxis_dict):

    result = []
    for series in series_data:
        new_series = json.loads(model)
        new_series['name'] = series['name']
        new_series['showPublishDate'] = series['showPublishDate']
        new_series['decimalPrecision'] = series['decimalPrecision']
        new_series['dataSet']['formula'] = series['expression']
        new_series['config']['name'] = series['label']
        new_series['config']['encode']['y'] = series['name']
        new_series['config']['datasetId'] = series['name']
        new_series['config']['itemStyle']['color'] = series['style']['color']
        new_series['config']['yAxisIndex'] = xAxis_dict.get(
            series['style']['y-axis']['name'], 0)
        new_series['config']['type'] = chartType.get(
            series['style']['chartType'], 'line')
        result.append(new_series)
    return result


with open(tabs_path, 'r', encoding='utf-8') as f:
    tabs_array = json.load(f)
    for tab_index, tab in enumerate(tabs_array):
        item = tab['visualization']['items'][0]
        series = item['visualization']['rows'][0]['series']
        all_series.append(convert_series(series, tab_xAxis_dict[tab_index]))

with open(new_tabs_path, 'w', encoding='utf-8') as new_f:
    json.dump(all_series, new_f, ensure_ascii=False, indent=2)
