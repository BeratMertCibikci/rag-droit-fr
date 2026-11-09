import json
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("BAAI/bge-m3")
maddeler = {m["numara"]: m for m in map(json.loads, open("data/rgpd.jsonl"))}

art4 = maddeler["4"]["metin"]
paragraf = next(s for s in art4.split("\n") if "pseudonymisation" in s)

soru = "Qu'est-ce que la pseudonymisation ?"
e = model.encode([soru, art4, paragraf], normalize_embeddings=True)
print("Soru ↔ tüm Article 4 :", round(float(e[0] @ e[1]), 3))
print("Soru ↔ tek paragraf  :", round(float(e[0] @ e[2]), 3))