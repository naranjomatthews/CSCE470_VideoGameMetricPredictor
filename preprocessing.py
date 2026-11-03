import json

with open("miniDataSet.json", "r", encoding="utf-8") as f:
    data = json.load(f)

print(json.dumps(data, ensure_ascii=True))
