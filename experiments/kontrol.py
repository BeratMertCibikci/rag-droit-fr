import json, numpy as np
from sentence_transformers import SentenceTransformer

parcalar = [json.loads(s) for s in open("data/rgpd_chunks.jsonl", encoding="utf-8")]
V = np.load("data/rgpd_vektorler.npy")
model = SentenceTransformer("BAAI/bge-m3")
q = model.encode("Qu'est-ce que le droit à l'oubli ?", normalize_embeddings=True)

benzerlik = V @ q
for i in np.argsort(-benzerlik)[:5]:
    print(parcalar[i]["id"], round(1 - benzerlik[i], 3))