import json

from qdrant_client import QdrantClient

qdrant_client = QdrantClient(
    url="https://83f966fe-104c-45b6-8141-6555d0cc972d.eu-west-1-0.aws.cloud.qdrant.io:6333", 
    api_key="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3MiOiJtIn0.u7z6adyaOgMLG0UcKhs2ogY4bV8PFiaBZY43nAxK9Co",
)

# Note: create collection only if it does not exist
try:
    qdrant_client.create_collection(
        collection_name="documents",
        vectors_config={
            "size": 1024,  # Size of the vector
            "distance": "Cosine"  # Distance metric
        }
    )
except Exception as e:
    print(f"Error creating collection: {e}")

index = 0
with open("data/chunks.jsonl", "r", encoding="utf-8") as cf:
    with open("data/embeddings.jsonl", "r", encoding="utf-8") as ef:
        for chunk, embedding in zip(cf, ef):
            chunk_line = chunk.strip()
            embedding_line = embedding.strip()
            
            chunk_data = json.loads(chunk_line)
            embedding_data = json.loads(embedding_line)

            qdrant_client.upsert(
                collection_name="documents",
                points=[{
                    "id": index,
                    "vector": embedding_data["embedding"],
                    "payload": chunk_data
                }]
            )
            
            index += 1
            print(f"Indexed chunk {index} with embedding.")