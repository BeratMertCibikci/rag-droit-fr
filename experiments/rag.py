from dotenv import load_dotenv
from litellm import completion
from db_ara import db_rerank as rerank_ara
from routing import madde_no_bul, madde_getir


SISTEM = """Tu es un assistant juridique. Réponds UNIQUEMENT à partir des sources fournies.
Après chaque information, indique la source entre crochets, par ex. [2].
Si les sources ne permettent pas de répondre, dis-le clairement. Réponds en français."""

ESIK = 0.05

def kaynaklari_bul(soru):
    no = madde_no_bul(soru)
    if no:
        parcalar = madde_getir(no)
        if parcalar:                                   # madde gerçekten varsa
            return "madde", parcalar
    sonuclar = rerank_ara(soru)
    if sonuclar[0][0] < ESIK:
        return "yok", []
    return "arama", [p for _, _, p in sonuclar]

def cevapla(soru):
    yol, parcalar = kaynaklari_bul(soru)
    if yol == "yok":
        no = madde_no_bul(soru)
        if no:
            print(f"L'article {no} n'existe pas dans le RGPD.")
        print("Les sources ne contiennent pas d'information sur cette question.")
        return
    kaynaklar = "\n\n".join(f"[{i}] {p['metin']}" for i, p in enumerate(parcalar, 1))
    cevap = completion(
        model="mistral/mistral-small-latest",
        messages=[{"role": "system", "content": SISTEM},
                  {"role": "user", "content": f"Sources :\n{kaynaklar}\n\nQuestion : {soru}"}])
    print(cevap.choices[0].message.content)
    print(f"\nYol: {yol} | Kaynaklar:")
    for i, p in enumerate(parcalar, 1):
        print(f"[{i}] {p['id']} | {p['url']}")
    print("Girdi token:", cevap.usage.prompt_tokens)
    
if __name__ == "__main__":
    for soru in ["Que dit l'article 17 ?",
                 "Qu'est-ce que le droit à l'oubli ?",
                 "Que dit l'article 999 sur l'oubli ?"]:
        print("\n########", soru)
        cevapla(soru)
    
