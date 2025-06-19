import json

from langchain_text_splitters import CharacterTextSplitter

with open("data/output.md", "rt", encoding="utf-8") as f:
    file_content = f.read()

text_splitter = CharacterTextSplitter(
    separator="\n\n",
    chunk_size=2000,
    chunk_overlap=100,
    length_function=len,
    is_separator_regex=False,
)

texts = text_splitter.create_documents([file_content])

print(f"Number of chunks: {len(texts)}")

print("First five chunks:")
for i, text in enumerate(texts[:5]):
    # Note: clean duplicate whitespace
    text.page_content = " ".join(text.page_content.split())
    print(f"Chunk {i + 1}:\n{text.page_content}\n")
    print("-" * 40)

# Note: write normalized chunks to file (format JSON lines)
with open("data/chunks.jsonl", "w", encoding="utf-8") as f:
    for text in texts:
        f.write(json.dumps({"text": " ".join(text.page_content.split())}, ensure_ascii=False) + "\n")
