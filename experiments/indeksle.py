import json, time
import numpy as np
from sentence_transformers import SentenceTransformer

parcalar = [json.loads(s) for s in open("data/rgpd_chunks.jsonl")]
model = SentenceTransformer("BAAI/bge-m3")

t = time.time()
vektorler = model.encode([p["metin"] for p in parcalar],
                         normalize_embeddings=True, show_progress_bar=True)
print(vektorler.shape, f"{time.time() - t:.1f} saniye")

np.save("data/rgpd_vektorler.npy", vektorler)