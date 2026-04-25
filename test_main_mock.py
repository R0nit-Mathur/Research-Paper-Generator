from chunker import chunk_document

def humanize_chunk(chunk):
    return "[HUMANIZED] " + chunk

def main():
    INPUT_FILE = "input.txt"
    OUTPUT_FILE = "output_mock.txt"

    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        text = f.read()

    items = chunk_document(text)
    print("Total items:", len(items))

    with open(OUTPUT_FILE, "w", encoding="utf-8") as out:
        for i, item in enumerate(items, 1):
            t = item["type"]
            content = item["text"]

            if t == "chunk":
                if len(content.split()) < 10:
                    print(f"Skipping item {i}/{len(items)} | {t} (Too Short: preserved verbatim)")
                    out.write(content + "\n\n")
                else:
                    print(f"Humanizing item {i}/{len(items)} | {t} (Sent to GPTInf)")
                    processed = humanize_chunk(content)
                    out.write(processed + "\n\n")
            else:
                print(f"Preserving structural item {i}/{len(items)} | {t}")
                out.write(content + "\n\n")

if __name__ == "__main__":
    main()
