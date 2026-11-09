import json
import numpy as np
from sentence_transformers import SentenceTransformer
import re, snowballstemmer
from rank_bm25 import BM25Plus
from sentence_transformers import CrossEncoder

reranker = CrossEncoder("BAAI/bge-reranker-v2-m3")   # ilk seferde ~2 GB iner

parcalar = [json.loads(s) for s in open("data/rgpd_chunks.jsonl")]
vektorler = np.load("data/rgpd_vektorler.npy")
model = SentenceTransformer("BAAI/bge-m3")

def rerank_ara(soru, aday=20, k=5):
    adaylar = hybrid_ara(soru, k=aday)
    skorlar = reranker.predict([(soru, p["metin"]) for _, _, p in adaylar])
    sirali = sorted(zip(skorlar, range(1, aday + 1), adaylar), key=lambda x: -x[0])
    return [(round(float(s), 3), h, p) for s, h, (_, _, p) in sirali[:k]]

stem = snowballstemmer.stemmer("french")
STOP = {"le","la","les","de","des","du","un","une","et","en","au","aux","qui","que",
        "qu","pour","ne","l","d","est","ce","ceux","être","on","peut","dit","combien"}
def tok(t):
    return [stem.stemWord(k) for k in re.findall(r"[\w-]+", t.lower()) if k not in STOP]

bm25 = BM25Plus([tok(p["metin"]) for p in parcalar])

def sira(skorlar):  # en yüksek skor = 1. sıra
    return {int(i): r + 1 for r, i in enumerate(np.argsort(-skorlar))}

def hybrid_ara(soru, k=5):
    q = model.encode([soru], normalize_embeddings=True)[0]
    rv = sira(vektorler @ q)
    rb = sira(bm25.get_scores(tok(soru)))
    rrf = np.array([1/(60 + rv[i]) + 1/(60 + rb[i]) for i in range(len(parcalar))])
    return [(rv[i], rb[i], parcalar[i]) for i in np.argsort(-rrf)[:k]]

def ara(soru, k=5):
    q = model.encode([soru], normalize_embeddings=True)[0]
    skorlar = vektorler @ q                    # soru ile 142 parçanın benzerliği
    en_iyiler = np.argsort(-skorlar)[:k]       # en yüksek k skorun sırası
    return [(round(float(skorlar[i]), 3), parcalar[i]) for i in en_iyiler]

# Burası en soldan başlamalı (0 boşluk)
if __name__ == "__main__":
    sorular = {
        "cevaplanabilir": ["Qu'est-ce que le droit à l'oubli ?",
                        "Combien de temps peut-on conserver des données personnelles ?",
                        "Qu'est-ce que la pseudonymisation ?",
                        "Que dit l'article 17 ?",
                        "Quand faut-il notifier une violation de données ?"],
        "cevaplanamaz":   ["Quel est le montant du salaire minimum en France ?",
                        "Combien de jours de congés payés a un salarié ?",
                        "Qui a gagné la Coupe du monde 2018 ?"],
    }
    
    # for döngüsü if bloğunun içinde olmalı (4 boşluk)
    for tur, liste in sorular.items():
        print(f"\n{'='*50}\nKATEGORİ: {tur.upper()}\n{'='*50}")
        for soru in liste:
            en_iyi = rerank_ara(soru, k=1)[0]
            skor = en_iyi[0]
            bulunan_metin = en_iyi[2]["metin"] # Chunk'ın asıl içeriği
            
            print(f"Soru: {soru}")
            print(f"Skor: {skor}")
            print(f"Cevap (Bulunan Metin):\n{bulunan_metin}\n")
            print("-" * 40)
