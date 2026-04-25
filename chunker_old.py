import re
import ftfy
import syntok.segmenter as segmenter

MIN_WORDS = 40
MAX_WORDS = None


# -------------------------------------
# NORMALIZATION
# -------------------------------------

def normalize_text(text):

    text = ftfy.fix_text(text)

    text = text.replace("\r\n","\n")

    text = re.sub(r"[ \t]+"," ",text)

    text = re.sub(r"-\n","",text)

    text = re.sub(r"\n{3,}","\n\n",text)

    return text.strip()


# -------------------------------------
# SENTENCE TOKENIZER (syntok)
# -------------------------------------

def split_sentences(text):

    sentences = []

    for paragraph in segmenter.process(text):

        for sentence in paragraph:

            s = " ".join([token.value for token in sentence])

            sentences.append(s)

    return sentences


# -------------------------------------
# HEADING DETECTION
# -------------------------------------

HEADINGS = {
"abstract","introduction","conclusion",
"references","keywords","discussion",
"results","method","methods"
}

def is_heading(text):

    t = text.strip()

    if not t:
        return False

    clean = t.lower().strip(":—- ")

    if clean in HEADINGS:
        return True

    if re.match(r"^\d+(\.\d+)*\s+[A-Z]",t):
        return True

    if len(t.split()) <= 8 and t.istitle():
        return True

    return False


# -------------------------------------
# EQUATION DETECTION
# -------------------------------------

def is_equation(text):

    t = text.strip()

    if len(t.split()) > 12:
        return False

    if re.search(r'\\(sum|frac|alpha|beta|gamma|theta)',t):
        return True

    if re.search(r'[a-zA-Z]\s*=\s*[a-zA-Z0-9]',t):
        return True

    if re.search(r'[a-zA-Z]_[a-zA-Z0-9]',t):
        return True

    if re.search(r'[a-zA-Z]\^[0-9]',t):
        return True

    if len(re.findall(r'[=+\-*/^]',t)) >= 3:
        return True

    return False


# -------------------------------------
# INLINE HEADING SPLIT
# -------------------------------------

def split_inline_heading(text):

    m = re.match(
        r'^(Abstract|Introduction|Conclusion|Keywords)\s*[—:-]\s*(.+)',
        text,
        re.I
    )

    if m:

        return [
            {"type":"heading","text":m.group(1)},
            {"type":"chunk","text":m.group(2)}
        ]

    return None


# -------------------------------------
# PARAGRAPH EXTRACTION
# -------------------------------------

def extract_paragraphs(text):

    lines = text.split("\n")

    paragraphs = []
    buffer = []

    for line in lines:

        line=line.strip()

        if not line:

            if buffer:

                paragraphs.append(" ".join(buffer))

                buffer=[]

            continue

        buffer.append(line)

    if buffer:

        paragraphs.append(" ".join(buffer))

    return paragraphs


# -------------------------------------
# CHUNK PARAGRAPH
# -------------------------------------

def chunk_paragraph(paragraph):

    if MAX_WORDS is None:

        return [paragraph]

    sentences = split_sentences(paragraph)

    chunks=[]
    current=[]
    words=0

    for s in sentences:

        w=len(s.split())

        if words+w>MAX_WORDS and words>=MIN_WORDS:

            chunks.append(" ".join(current))

            current=[]
            words=0

        current.append(s)

        words+=w

    if current:

        if words<MIN_WORDS and chunks:

            chunks[-1]+= " " + " ".join(current)

        else:

            chunks.append(" ".join(current))

    return chunks


# -------------------------------------
# MAIN CHUNKER
# -------------------------------------

def chunk_document(text):

    text = normalize_text(text)

    paragraphs = extract_paragraphs(text)

    output=[]

    for para in paragraphs:

        p = para.strip()

        inline = split_inline_heading(p)

        if inline:

            output.extend(inline)

            continue

        if is_heading(p):

            output.append({"type":"heading","text":p})

            continue

        if is_equation(p):

            output.append({"type":"equation","text":p})

            continue

        chunks = chunk_paragraph(p)

        for c in chunks:

            output.append({"type":"chunk","text":c})

    return output