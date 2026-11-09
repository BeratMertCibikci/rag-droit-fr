import requests
from bs4 import BeautifulSoup

url = "https://eur-lex.europa.eu/legal-content/FR/TXT/HTML/?uri=CELEX:32016R0679"
html = requests.get(url, timeout=30).text
open("experiments/rgpd.html", "w").write(html)  # tekrar tekrar indirmemek için
soup = BeautifulSoup(html, "html.parser")

basliklar = soup.find_all("p", class_="oj-ti-art")
print("Madde sayısı:", len(basliklar))

b = basliklar[5]  # Article 6
print("Başlık:", b.get_text())
print("Ebeveyn:", b.parent.name, b.parent.get("id"), b.parent.get("class"))
for kardes in b.find_next_siblings()[:4]:
    print("  Kardeş:", kardes.name, kardes.get("id"), kardes.get("class"), kardes.get_text()[:60])