import re
import psycopg

URL = "postgresql://rag:rag@localhost:5432/rag"

def madde_getir(no):
    with psycopg.connect(URL) as conn:
        satirlar = conn.execute(
            "SELECT id, metin, url FROM chunks WHERE madde = %s ORDER BY id", (no,))
        return [{"id": r[0], "metin": r[1], "url": r[2]} for r in satirlar]

for no in ["17", "4", "999"]:
    print(no, "→", [p["id"] for p in madde_getir(no)])

def madde_no_bul(soru):
    eslesme = re.search(r"\bart(?:icle)?\.?\s*(\d+)", soru, re.IGNORECASE)
    return eslesme.group(1) if eslesme else None

if __name__ == "__main__":
    for soru in ["Que dit l'article 17 ?",
                "Que dit l'art. 17 ?",
                "art 6 RGPD",
                "Je suis un artiste",
                "Qu'est-ce que le droit à l'oubli ?"]:
        print(repr(madde_no_bul(soru)), "←", soru)