from bs4 import BeautifulSoup

# Yerel dosyayı okuyoruz
try:
    with open("experiments/aiact.html", "r", encoding="utf-8") as f:
        html = f.read()
except FileNotFoundError:
    print("Hata: 'experiments/aiact.html' dosyası bulunamadı. Lütfen tarayıcıdan indirip bu konuma kaydedin.")
    exit()

soup = BeautifulSoup(html, "html.parser")

maddeler = [k for k in soup.find_all("div", class_="eli-subdivision") if k.get("id", "").startswith("art_")]


print(f"Toplam {len(html)} karakter okundu.")
print(f"Bulunan madde sayısı: {len(maddeler)}")

if maddeler:
    print("İlk:", maddeler[0].get("id"), "| Son:", maddeler[-1].get("id"))
else:
    print("\nHiç madde bulunamadı! Lütfen aiact.html dosyasını bir metin editöründe açın ve 'Article premier' veya 'Article 2' yazan yerin etrafındaki HTML class/id yapısına bakın.")
