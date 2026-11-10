from bs4 import BeautifulSoup
import json

EURLEX = "https://eur-lex.europa.eu/legal-content/FR/TXT/HTML/?uri=CELEX:"
KAYNAKLAR = [("RGPD", "experiments/rgpd.html", "32016R0679"),
             ("AI Act", "experiments/aiact.html", "32024R1689")]

def kutuyu_oku(kutu, kaynak, url):
    id_ = kutu.get("id")                       # "art_17" veya "anx_III"
    numara = id_.removeprefix("art_") if id_.startswith("art_") else "Annexe " + id_.removeprefix("anx_")
    s = satirlari_al(kutu)
    return {"kaynak": kaynak, "numara": numara,
            "baslik": s[0], "alt_baslik": s[1],
            "metin": "\n".join(s[2:]), "url": url + "#" + id_}

def parse_et(kaynak, dosya, celex):
    soup = BeautifulSoup(open(dosya, encoding="utf-8").read(), "html.parser")
    kutular = [k for k in soup.find_all("div", class_=["eli-subdivision", "eli-container"])
               if k.get("id", "").startswith(("art_", "anx_"))]
    return [kutuyu_oku(k, kaynak, EURLEX + celex) for k in kutular]

def satirlari_al(kutu):
    satirlar = []
    for el in kutu.find_all(["p", "tr"]):
        if el.find_parent("tr"):            # bir tablo satırının içinde: üstteki satırda zaten var
            continue
        metin = el.get_text(" ", strip=True)
        if metin:
            satirlar.append(metin)
    return satirlar





for kaynak, dosya, celex in KAYNAKLAR:
    m = parse_et(kaynak, dosya, celex)
    print(f"{kaynak}: {len(m)} madde | {m[5]['baslik']}: {m[5]['alt_baslik']}")
    
with open("data/maddeler.jsonl", "w", encoding="utf-8") as f:
    for kaynak, dosya, celex in KAYNAKLAR:
        maddeler = parse_et(kaynak, dosya, celex)
        print(kaynak, len(maddeler))
        for m in maddeler:
            f.write(json.dumps(m, ensure_ascii=False) + "\n")