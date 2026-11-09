import psycopg
from pgvector.psycopg import register_vector
from sentence_transformers import SentenceTransformer
from sentence_transformers import CrossEncoder

reranker = CrossEncoder("BAAI/bge-reranker-v2-m3")
model = SentenceTransformer("BAAI/bge-m3")
URL = "postgresql://rag:rag@localhost:5432/rag"

def db_hybrid(soru, k=20):
    q = model.encode(soru, normalize_embeddings=True)
    with psycopg.connect(URL) as conn:
        register_vector(conn)
        vek = [r[0] for r in conn.execute(
            "SELECT id FROM chunks ORDER BY embedding <=> %s LIMIT %s", (q, k))]
        bm = [r[0] for r in conn.execute(
            "SELECT id FROM chunks WHERE metin ||| %s ORDER BY pdb.score(id) DESC, id LIMIT %s", (soru, k))]
    skor = {}
    for liste in (vek, bm):
        for sira, id_ in enumerate(liste, 1):
            skor[id_] = skor.get(id_, 0) + 1 / (60 + sira)
    return sorted(skor.items(), key=lambda x: -x[1])

def db_rerank(soru, aday=20, k=5):
    idler = [id_ for id_, _ in db_hybrid(soru)[:aday]]
    with psycopg.connect(URL) as conn:
        satirlar = conn.execute("SELECT id, metin, url FROM chunks WHERE id = ANY(%s)", (idler,))
        bulunan = {r[0]: {"id": r[0], "metin": r[1], "url": r[2]} for r in satirlar}
    parcalar = [bulunan[i] for i in idler]
    skorlar = reranker.predict([(soru, p["metin"]) for p in parcalar])
    sonuc = [(s, sira, p) for sira, (s, p) in enumerate(zip(skorlar, parcalar), 1)]
    return sorted(sonuc, key=lambda x: -x[0])[:k]

if __name__ == "__main__":
    for id_, s in db_hybrid("Qu'est-ce que le droit à l'oubli ?")[:5]:
        print(id_, round(s, 4))
