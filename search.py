import json
import faiss
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")
index = faiss.read_index("index.faiss")
chunks = json.load(open("chunks.json", encoding="utf-8"))

def _raw_retrieve(question, k=4):
    q = model.encode([question], normalize_embeddings=True)
    scores, ids = index.search(q, k)
    return [(float(s), chunks[i]) for s, i in zip(scores[0], ids[0])]

if __name__ == "__main__":
    while True:
        question = input("\nAsk a question (or type quit): ")
        if question.strip().lower() == "quit":
            break
        for score, c in retrieve(question):
            print(f"\n[{score:.2f}] {c['source']} page {c['page']}")
            print(c["text"][:300], "...")
def retrieve(question, k=5):
    raw = _raw_retrieve(question, k=k * 4)
    seen, out = set(), []
    for score, chunk in raw:
        key = (chunk["source"], chunk["page"])
        if key in seen:
            continue
        seen.add(key)
        out.append((score, chunk))
    return out[:k]