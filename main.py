from chunker import chunk_document
from humanizer import humanize_chunk


def main():

    INPUT_FILE = "input.txt"
    OUTPUT_FILE = "output.txt"

    # read input document
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        text = f.read()

    # generate structured chunks
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
                    try:
                        processed = humanize_chunk(content)
                    except Exception as e:
                        print("Chunk failed:", e)
                        processed = content

                    out.write(processed + "\n\n")

            else:
                # tags, headings, equations, images all go directly without humanizing
                print(f"Preserving structural item {i}/{len(items)} | {t}")
                out.write(content + "\n\n")

    print("Finished. Output saved to", OUTPUT_FILE)


if __name__ == "__main__":
    main()