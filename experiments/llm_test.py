from dotenv import load_dotenv
from litellm import completion

load_dotenv()   # .env dosyasındaki MISTRAL_API_KEY'i okur

cevap = completion(
    model="mistral/mistral-small-latest",
    messages=[{"role": "user", "content": "En une phrase, qu'est-ce que le RGPD ?"}],
)
print(cevap.choices[0].message.content)
print("Girdi token:", cevap.usage.prompt_tokens, "| Çıktı token:", cevap.usage.completion_tokens)