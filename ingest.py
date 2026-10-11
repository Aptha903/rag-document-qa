import re, json
from pathlib import Path
from pypdf import PdfReader
from sentence_transformers import SentenceTransformer
import faiss

JUNK = [r"VTUADDA", r"AZ Documents?", r"www\.azdocuments\.in",
        r"1BPLC105B/205B PYTHON PROGRAMMING", r"MODULE-0\d", r"^\s*\d+\s*$"]

def clean(text):
    lines = []
    for line in text.splitlines():
        if any(re.search(p, line.strip()) for p in JUNK):
            continue
        lines.append(line.strip())
    return re.sub(r"\s+", " ", " ".join(lines)).strip()

def split(text, size=800, overlap=150):
    out, start = [], 0
    while start < len(text):
        out.append(text[start:start + size])
        start += size - overlap
    return out

chunks = []
for pdf in sorted(Path("docs").glob("*.pdf")):
    reader = PdfReader(pdf)
    for page_no, page in enumerate(reader.pages, start=1):
        text = clean(page.extract_text() or "")
        if len(text) < 50:
            continue
        for piece in split(text):
            chunks.append({"source": pdf.name, "page": page_no, "text": piece})

print("Total chunks:", len(chunks))

model = SentenceTransformer("all-MiniLM-L6-v2")
vectors = model.encode([c["text"] for c in chunks], normalize_embeddings=True, show_progress_bar=True)

index = faiss.IndexFlatIP(vectors.shape[1])
index.add(vectors)
faiss.write_index(index, "index.faiss")
json.dump(chunks, open("chunks.json", "w", encoding="utf-8"), ensure_ascii=False)

print("Saved index.faiss and chunks.json")
print("Sample chunk:", chunks[10]["source"], "page", chunks[10]["page"])
print(chunks[10]["text"])