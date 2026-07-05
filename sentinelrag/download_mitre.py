import requests, json

url = "https://raw.githubusercontent.com/mitre/cti/master/enterprise-attack/enterprise-attack.json"
print("Downloading MITRE ATT&CK...")
r = requests.get(url)
data = r.json()

techniques = []
for obj in data['objects']:
    if obj['type'] == 'attack-pattern':
        techniques.append({
            'id': obj.get('external_references', [{}])[0].get('external_id', ''),
            'name': obj.get('name', ''),
            'description': obj.get('description', '')[:500],
            'detection': obj.get('x_mitre_detection', '')[:300]
        })

with open('knowledge/mitre_techniques.json', 'w') as f:
    json.dump(techniques, f, indent=2)

print("Downloaded", len(techniques), "techniques")
