from chunker import chunk_document

if __name__ == "__main__":
    with open("input.txt", "r", encoding="utf-8") as f:
        text = f.read()
        
    chunks = chunk_document(text)
    
    for i, chunk in enumerate(chunks[:10]):
        print(f"[{i}] TYPE: {chunk['type']}")
        print(chunk['text'][:100] + "...\n")
        
    print(f"Total chunks: {len(chunks)}")
