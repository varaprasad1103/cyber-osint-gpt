import json

with open('data/processed/processed_incidents.json', encoding='utf-8') as f:
    data = json.load(f)

for idx in [3, 6, 7]:
    inc = data[idx]
    print(f"=== Article {idx+1}: {inc['title']} ===")
    print(inc['cleaned_text'][:400])
    print()