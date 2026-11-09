import json, numpy as np, psycopg
from pgvector.psycopg import register_vector

parcalar = [json.loads(s) for s in open("data/rgpd_chunks.jsonl", encoding="utf-8")]
vektorler = np.load("data/rgpd_vektorler.npy")

with psycopg.connect("postgresql://rag:rag@localhost:5432/rag") as conn:
    register_vector(conn)
    for p, v in zip(parcalar, vektorler):
        conn.execute(
            "INSERT INTO chunks (id, kaynak, madde, url, metin, embedding) "
            "VALUES (%s, %s, %s, %s, %s, %s) ON CONFLICT (id) DO NOTHING",
            (p["id"], p["kaynak"], p["madde"], p["url"], p["metin"], v))
    print(conn.execute("SELECT count(*) FROM chunks").fetchone())