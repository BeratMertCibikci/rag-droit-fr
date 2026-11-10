import re
import psycopg

URL = "postgresql://rag:rag@localhost:5432/rag"

def madde_getir(no, kaynak=None):
    sql, params = "SELECT id, metin, url, kaynak FROM chunks WHERE madde = %s", [no]
    if kaynak:                                   # kanun belliyse filtreye ekle
        sql += " AND kaynak = %s"
        params.append(kaynak)
    with psycopg.connect(URL) as conn:
        satirlar = conn.execute(sql + " ORDER BY id", params)
        return [{"id": r[0], "metin": r[1], "url": r[2], "kaynak": r[3]} for r in satirlar]

def madde_no_bul(soru):
    eslesme = re.search(r"\bart(?:icle)?\.?\s*(\d+)", soru, re.IGNORECASE)
    return eslesme.group(1) if eslesme else None

KAYNAK_KALIPLARI = {"AI Act": r"\b(ai act|ria)\b|intelligence artificielle",
                    "RGPD":   r"\b(rgpd|gdpr)\b"}

def kaynak_bul(soru):
    for kaynak, kalip in KAYNAK_KALIPLARI.items():
        if re.search(kalip, soru, re.IGNORECASE):
            return kaynak
    return None


if __name__ == "__main__":
    for soru in ["Que dit l'article 6 du RGPD ?",
                 "Que dit l'article 6 de l'AI Act ?",
                 "Que dit l'article 6 ?",
                 "article 99 du règlement sur l'intelligence artificielle"]:
        no, kaynak = madde_no_bul(soru), kaynak_bul(soru)
        print(f"{no} {kaynak!s:7} {[p['id'] for p in madde_getir(no, kaynak)]}  ← {soru}")