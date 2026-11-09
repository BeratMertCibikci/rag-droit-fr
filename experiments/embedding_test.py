from sentence_transformers import SentenceTransformer
import re, snowballstemmer

model = SentenceTransformer("BAAI/bge-m3")
cumleler = [
    "Article L4121-1 : L'employeur prend les mesures nécessaires pour assurer la sécurité et protéger la santé des travailleurs.",
    "Article L4121-2 : L'employeur met en oeuvre les mesures de prévention en évitant les risques et en évaluant ceux qui ne peuvent être évités.",
    "Article L4121-3 : L'employeur évalue les risques pour la santé et la sécurité des travailleurs.",
    "Article 5 RGPD : Les données personnelles sont conservées pour une durée limitée.",
]
emb = model.encode(cumleler, normalize_embeddings=True)
print(emb.shape)
print((emb @ emb.T).round(2))

from rank_bm25 import BM25Plus
soru = "Qui doit évaluer les risques au travail ?"
bm25 = BM25Plus([c.lower().split() for c in cumleler])
bm25_skor = bm25.get_scores(soru.lower().split())
vek_skor = emb @ model.encode([soru], normalize_embeddings=True)[0]

stem = snowballstemmer.stemmer("french")
STOP = {"le","la","les","de","des","du","un","une","et","en","au","aux",
        "qui","que","pour","ne","l","d","est","ceux","être"}
def tok(t):
    kelimeler = re.findall(r"[\w-]+", t.lower())
    return [stem.stemWord(k) for k in kelimeler if k not in STOP]

bm25 = BM25Plus([tok(c) for c in cumleler])
bm25_skor = bm25.get_scores(tok(soru))

def sira(skorlar):  # en yüksek skor = 1. sıra
    s = sorted(range(len(skorlar)), key=lambda i: -skorlar[i])
    return {i: r + 1 for r, i in enumerate(s)}

rv, rb = sira(vek_skor), sira(bm25_skor)
print("vek :", vek_skor.round(3))
print("bm25:", bm25_skor.round(3))
for i, c in enumerate(cumleler):
    rrf = 1/(60 + rv[i]) + 1/(60 + rb[i])
    print(f"{rrf:.4f}  vek#{rv[i]}  bm25#{rb[i]}  {c[:45]}")
    
