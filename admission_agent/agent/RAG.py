import faiss
from sentence_transformers import SentenceTransformer
import json
from openai import OpenAI
import jieba
from rank_bm25 import BM25Okapi
from collections import defaultdict
from sentence_transformers import CrossEncoder
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INDEX_PATH=os.path.join(BASE_DIR, "szu_admission.index")
CHUNKS_PATH=os.path.join(BASE_DIR,"szu_admission_chunks.json")

reranker = CrossEncoder("BAAI/bge-reranker-large")

client = OpenAI(
    api_key="sk-28d199a5c79f45718b955a255d771bd1",
    base_url="https://api.deepseek.com"
)

# embedding 模型（必须和之前一致）
model = SentenceTransformer("BAAI/bge-m3")

# index
index = faiss.read_index(INDEX_PATH)

def tokenize(text):
    return list(jieba.cut(text))

def bm25_retrieve(query, chunks, bm25, top_k=20):
    tokenized_query = tokenize(query)
    scores = bm25.get_scores(tokenized_query)

    ranked = sorted(
        enumerate(scores),
        key=lambda x: x[1],
        reverse=True
    )[:top_k]

    results = []
    for idx, score in ranked:
        results.append({
            "idx": idx,
            "score": float(score),
            "text": chunks[idx]["text"],
            "source": chunks[idx].get("source", "")
        })
    return results


def build_context(retrieved_chunks):
    context = ""
    for i, r in enumerate(retrieved_chunks):
        context += f"""【资料{i+1}】
        {r["text"]}
        """
    return context

def build_prompt(query, retrieved_chunks):
    context = build_context(retrieved_chunks)
    prompt = f"""
    你是深圳大学招生问答助手。

    请仅根据下面给出的资料回答用户问题。
    - 如果资料中完全没有相关信息，才回答：“根据现有资料无法确定”。
    - 允许对资料中的表格、汇总信息进行对应、整理和直接引用，但不得引入资料之外的内容。
    
    【资料】
    {context}
    
    【问题】
    {query}
    
    【回答要求】
    - 用简体中文
    - 回答要准确、简洁
    - 答案必须能在资料中找到直接依据（可引用资料编号）
    - 保持自然的段落换行，不要输出任何 Markdown 的加粗符号（如 **）
    """
    return prompt,context

def vector_retrieve(query, chunks, top_k=20):
    q_emb = model.encode([query], normalize_embeddings=True)
    scores, indices = index.search(q_emb, top_k)

    results = []
    for score, idx in zip(scores[0], indices[0]):
        results.append({
            "idx": idx,
            "score": float(score),
            "text": chunks[idx]["text"],
            "source": chunks[idx].get("source", "")
        })
    return results

def rrf_fusion(vec_results, bm25_results, k=60, top_k=5):
    scores = defaultdict(float)
    doc_map = {}

    for rank, r in enumerate(vec_results):
        scores[r["idx"]] += 1 / (k + rank + 1)
        doc_map[r["idx"]] = r

    for rank, r in enumerate(bm25_results):
        scores[r["idx"]] += 1 / (k + rank + 1)
        doc_map[r["idx"]] = r

    ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)

    return [doc_map[idx] for idx, _ in ranked[:top_k]]

def rerank(query, docs, top_k=5):
    pairs = [(query, d["text"]) for d in docs]
    scores = reranker.predict(pairs)

    for d, s in zip(docs, scores):
        d["rerank_score"] = float(s)

    docs = sorted(docs, key=lambda x: x["rerank_score"], reverse=True)
    return docs[:top_k]

def rag_answer(query):
    with open(CHUNKS_PATH,'r',encoding="utf-8") as f:
        chunks=json.load(f)
    tokenized_corpus = [tokenize(c["text"]) for c in chunks]
    bm25 = BM25Okapi(tokenized_corpus)
    vec_results = vector_retrieve(query, chunks, top_k=20)
    bm25_results = bm25_retrieve(query, chunks, bm25, top_k=20)
    retrieved = rrf_fusion(vec_results, bm25_results, top_k=20)
    retrieved = rerank(query, retrieved,top_k=20)
    prompt,context = build_prompt(query, retrieved)
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": "你是一个严谨的招生问答助手。"},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2,
    )
    return response.choices[0].message.content,context