import json

maddeler = [json.loads(satir) for satir in open("data/rgpd.jsonl")]
uzunluklar = sorted((len(m["metin"].split()), m["numara"]) for m in maddeler)

print("En kısa 3:", uzunluklar[:3])
print("En uzun 3:", uzunluklar[-3:])