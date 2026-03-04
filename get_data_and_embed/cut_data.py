import json
from tqdm import tqdm

def chunk_text(text, max_len=400):
    paragraphs = text.split("\n")
    chunks = []
    current = ""

    for p in paragraphs:
        if len(current) + len(p) <= max_len:
            current += p + "\n"
        else:
            chunks.append(current.strip())
            current = p + "\n"

    if current.strip():
        chunks.append(current.strip())

    return chunks

rag_docs = []

with open("./szu_admission_articles_clean.json",'r',encoding="utf-8") as f:
    for item in tqdm(json.load(f)):  # 你那 405 条
        chunks = chunk_text(item["content"])
        for i, chunk in enumerate(chunks):
            rag_docs.append({
                "text": chunk,
                "title": item["title"],
                "url": item["url"],
                "chunk_id": i
            })

with open("szu_admission_chunks.json",'w',encoding="utf-8") as f:
    json.dump(rag_docs,f)