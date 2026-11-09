from dotenv import load_dotenv
from litellm import completion
from ara import rerank_ara

load_dotenv()

SISTEM = """Tu es un assistant juridique. Réponds UNIQUEMENT à partir des sources fournies.
Après chaque information, indique la source entre crochets, par ex. [2].
Si les sources ne permettent pas de répondre, dis-le clairement. Réponds en français."""

def cevapla(soru):
    sonuclar = rerank_ara(soru)
    ESIK = 0.05
    if sonuclar[0][0] < ESIK:
        print(f"Les sources ne contiennent pas d'information sur cette question. (skor: {sonuclar[0][0]})")
        return
    kaynaklar = "\n\n".join(f"[{i}] {p['metin']}" for i, (_, _, p) in enumerate(sonuclar, 1))
    cevap = completion(
        model="mistral/mistral-small-latest",
        messages=[{"role": "system", "content": SISTEM},
                  {"role": "user", "content": f"Sources :\n{kaynaklar}\n\nQuestion : {soru}"}],
    )
    print(cevap.choices[0].message.content)
    print("\nKaynaklar:")
    for i, (_, _, p) in enumerate(sonuclar, 1):
        print(f"[{i}] {p['id']} | {p['url']}")
    print("Girdi token:", cevap.usage.prompt_tokens)

for soru in ["Combien de temps peut-on conserver des données personnelles ?",
             "Quel est le montant du salaire minimum en France ?"]:
    print("\n########", soru)
    cevapla(soru)