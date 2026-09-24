import json

summery = '''
{
    "label": null,
    "enableGateClosure": false,
    "timezone": "",
    "beforeGateOffset": 0,
    "gateIndex": 0,
    "summary": "",
    "subtotalLabel": "GrandTotal",
    "subtotal": null,
    "beforeGate": null,
    "afterGate": null,
    "curveAction": {
        "curvePhase": 0,
        "curveName": "",
        "saveCurve": false
    },
    "subtotalFormula": "add(?)",
    "saveSubtotal": false
}
'''

path = "C:\\Users\\Sadiul Hakim\\OneDrive\\Desktop\\Report\\Report-2026 SEIN Meter Data Report Final (Fin) Per Entity.json"
new_path = "C:\\Users\\Sadiul Hakim\\OneDrive\\Desktop\\Report\\Report-2026 SEIN Meter Data Report Final (Fin) Per Entity New.json"

with open(path, "r", encoding='utf-8') as file:
    report = json.load(file)
    structure = report['structure']
    visualization = structure['visualizations'][0]
    row = visualization['rows'][0]
    series = row['series']

    for s in series:
        if s['name'] == 'Date' or len(s['summaries']) != 0:
            continue

        s['summaries'].append(json.loads(summery))

    with open(new_path, 'w', encoding='utf-8') as new_f:
        json.dump(report, new_f, ensure_ascii=False)
