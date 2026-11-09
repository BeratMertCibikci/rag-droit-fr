import json
from pathlib import Path
from bs4 import BeautifulSoup


html = open("experiments/rgpd.html").read()
soup = BeautifulSoup(html, "html.parser")

maddeler = []
for kutu in soup.find_all("div", class_="eli-subdivision"):
    isim = kutu.get("id")
    if isim.startswith("art_"):
        maddeler.append(kutu)

print(len(maddeler))
print(maddeler[0].get("id"), maddeler[-1].get("id"))

kutu = maddeler[5]   # 0'dan saydığımız için 5 = Article 6

numara = kutu.get("id").removeprefix("art_")
baslik = kutu.find("p", class_="oj-ti-art").get_text(strip=True)
alt_baslik = kutu.find("div", class_="eli-title").get_text(strip=True)

print(numara, "|", baslik, "|", alt_baslik)

paragraflar = []
for p in kutu.find_all("p", class_="oj-normal"):
    paragraflar.append(p.get_text(" ", strip=True))

metin = "\n".join(paragraflar)
print(len(paragraflar), "paragraf")
print(metin[:600])

URL = "https://eur-lex.europa.eu/legal-content/FR/TXT/HTML/?uri=CELEX:32016R0679"

def maddeyi_oku(kutu):
    paragraflar = [p.get_text(" ", strip=True)
                   for p in kutu.find_all("p", class_="oj-normal")]
    return {
        "kaynak": "RGPD",
        "numara": kutu.get("id").removeprefix("art_"),
        "baslik": kutu.find("p", class_="oj-ti-art").get_text(strip=True),
        "alt_baslik": kutu.find("div", class_="eli-title").get_text(strip=True),
        "metin": "\n".join(paragraflar),
        "url": URL + "#" + kutu.get("id"),
    }
sonuclar = [maddeyi_oku(kutu) for kutu in maddeler]

with open("data/rgpd.jsonl", "w") as f:
    for m in sonuclar:
        f.write(json.dumps(m, ensure_ascii=False) + "\n")

print(len(sonuclar), "madde kaydedildi")