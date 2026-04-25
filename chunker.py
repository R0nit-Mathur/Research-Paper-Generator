import re
import ftfy
import syntok.segmenter as segmenter

MIN_WORDS = 30
MAX_WORDS = 110


# ------------------------------------------------
# NORMALIZATION
# ------------------------------------------------

def normalize_text(text):

    text = ftfy.fix_text(text)

    text = text.replace("\r\n","\n")

    text = re.sub(r"[ \t]+"," ",text)

    text = re.sub(r"\n{3,}","\n\n",text)

    return text.strip()


# ------------------------------------------------
# SENTENCE SPLITTER
# ------------------------------------------------

def split_sentences(text):

    sentences=[]

    for paragraph in segmenter.process(text):

        for sentence in paragraph:

            s=" ".join([token.value for token in sentence])

            sentences.append(s)

    return sentences


# ------------------------------------------------
# HEADING DETECTION
# ------------------------------------------------

def is_heading(text):
    t = text.strip()
    # Check for Markdown headings
    if re.match(r'^#{1,6}\s+.+', t):
        return True
    return False

# ------------------------------------------------
# SPECIAL TAG DETECTION (@ABSTRACT, @KEYWORDS, @REFERENCES)
# ------------------------------------------------

def is_special_tag(text):
    t = text.strip()
    if t in ["@ABSTRACT", "@KEYWORDS", "@REFERENCES"]:
        return True
    return False


# ------------------------------------------------
# EQUATION DETECTION
# ------------------------------------------------

def is_equation(text):
    t = text.strip()
    
    # Check for block equation markers
    if t == "$$" or t.startswith("$$"):
        return True
        
    return False


# ------------------------------------------------
# PARAGRAPH EXTRACTION
# ------------------------------------------------

def extract_paragraphs(text):

    lines=text.split("\n")

    paragraphs=[]
    buffer=[]

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


# ------------------------------------------------
# CHUNK PARAGRAPH
# ------------------------------------------------

def chunk_paragraph(paragraph):

    if MAX_WORDS is None:
        return [paragraph]

    sentences=split_sentences(paragraph)

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


# ------------------------------------------------
# MAIN CHUNKER
# ------------------------------------------------

def chunk_document(text):
    text = normalize_text(text)
    paragraphs = extract_paragraphs(text)
    
    output = []
    
    in_block_equation = False
    equation_buffer = []

    for para in paragraphs:
        p = para.strip()
        
        # Handle multi-line block equations ($$ ... $$)
        if p == "$$":
            if not in_block_equation:
                in_block_equation = True
                equation_buffer = ["$$"]
                continue
            else:
                in_block_equation = False
                equation_buffer.append("$$")
                output.append({"type": "equation", "text": "\n".join(equation_buffer)})
                equation_buffer = []
                continue
                
        if in_block_equation:
            equation_buffer.append(p)
            continue

        if is_special_tag(p):
            output.append({"type": "special_tag", "text": p})
            continue

        if is_heading(p):
            # Strip the markdown hashes for the chunk type text
            clean_heading = re.sub(r'^#{1,6}\s+', '', p)
            output.append({"type": "heading", "text": clean_heading})
            continue
            
        # Check for image markdown
        if re.match(r'^!\[.*?\]\(.*?\)$', p):
            output.append({"type": "image", "text": p})
            continue

        chunks = chunk_paragraph(p)

        for c in chunks:
            output.append({"type": "chunk", "text": c})

    return output   