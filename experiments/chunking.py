import json

import re

def satirlari_birlestir(satirlar):
    sonuc = []
    for s in satirlar:
        if sonuc and re.fullmatch(r"\(?\w{1,4}\)", sonuc[-1]):
            sonuc[-1] = sonuc[-1] + " " + s   # önceki satır sadece "a)" ise, bu satırı ona ekle
        else:
            sonuc.append(s)
    return sonuc

SINIR = 300
maddeler = [json.loads(s) for s in open("data/maddeler.jsonl", encoding="utf-8")]

def paketle(satirlar, sinir=SINIR, sert_sinir=600):
    paketler, mevcut, giris = [], [], None
    for s in satirlar:
        kelime = len(" ".join(mevcut).split())
        yeni_paragraf = re.match(r"\d+[.)]\s", s)        # "2.   ..." veya "16) ..."
        liste_maddesi = re.match(r"\(?[a-z]{1,4}\)\s", s) # "a) ..." veya "iv) ..."

        if mevcut and ((yeni_paragraf and kelime > sinir) or
                       (liste_maddesi and kelime > sert_sinir)):
            paketler.append("\n".join(mevcut))
            mevcut = [giris + " (suite)"] if (liste_maddesi and giris) else []

        if yeni_paragraf:
            giris = None            # yeni paragraf: eski giriş cümlesi artık geçersiz
        if s.rstrip().endswith(":"):
            giris = s               # ":" ile biten satır = bir listenin giriş cümlesi
        mevcut.append(s)
    if mevcut:
        paketler.append("\n".join(mevcut))
    return paketler

def parcala(m):
    adres = f"{m['kaynak']} > {m['baslik']} > {m['alt_baslik']}"
    onek = m["kaynak"].lower().replace(" ", "")         # "RGPD" → "rgpd", "AI Act" → "aiact"
    no = m["numara"].replace(" ", "-")                  # "Annexe III" → "Annexe-III"
    if len(m["metin"].split()) <= SINIR:
        parcalar = [m["metin"]]            # kısa: tek parça
    else:
        parcalar = paketle(satirlari_birlestir(m["metin"].split("\n")))  # uzun: satır satır
    return [{"id": f"{onek}-{no}-{i}",
            "kaynak": m["kaynak"],
            "madde": m["numara"],
            "url": m["url"],
            "metin": adres + "\n" + p}
        for i, p in enumerate(parcalar)]

hepsi = [parca for m in maddeler for parca in parcala(m)]
print(len(hepsi), "parça")

    
with open("data/chunks.jsonl", "w") as f:
    for c in hepsi:
        f.write(json.dumps(c, ensure_ascii=False) + "\n")
print(len(hepsi), "parça kaydedildi")
print(hepsi[0]["id"], "|", hepsi[0]["metin"][:100])