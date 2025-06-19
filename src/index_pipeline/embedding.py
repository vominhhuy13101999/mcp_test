import json
import requests

url = 'https://api.jina.ai/v1/embeddings'
headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer jina_5612ecc3cf9944ea9c73e691f971525bZ9qpz_M9z58GwQVEoCxN_IxJV2Oz'
}

data = {
    "model": "jina-embeddings-v3",
    "task": "retrieval.passage",
    "input": []
}

batch_size = 10
batches = [[]]
with open("data/chunks.jsonl", "rt", encoding="utf-8") as f:
    for line in f.readlines():
        batches[-1].append(json.loads(line)["text"])
        if len(batches[-1]) == batch_size:
            batches.append([])

with open("data/embeddings.jsonl", "w", encoding="utf-8") as f:
    for batch in batches:
        data["input"] = batch
        response = requests.post(url, headers=headers, json=data)
        embeddings_data = response.json()["data"]
        for embedding_data in embeddings_data:
            embedding_data.pop("object")
            embedding_data.pop("index")
            f.write(json.dumps(embedding_data, ensure_ascii=False) + "\n")