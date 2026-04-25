import re
import os

def read_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.read()

def write_file(filepath, content):
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

def extract_sections(text):
    """
    Extracts dynamic sections from the text based on strict formatting rules.
    """
    sections = {
        'abstract': '',
        'keywords': '',
        'body': '',
        'references': []
    }
    
    # 1. Extract Abstract (everything after @ABSTRACT until the next @ or # tag)
    abs_match = re.search(r'@ABSTRACT\s*\n(.*?)(?=\n@|\n#|$)', text, re.IGNORECASE | re.DOTALL)
    if abs_match:
        sections['abstract'] = abs_match.group(1).strip()
        
    # 2. Extract Keywords
    kw_match = re.search(r'@KEYWORDS\s*\n(.*?)(?=\n@|\n#|$)', text, re.IGNORECASE | re.DOTALL)
    if kw_match:
        sections['keywords'] = kw_match.group(1).strip()
        
    # 3. Extract References
    ref_match = re.search(r'@REFERENCES\s*\n(.*?)(?=\n@|\n#|$)', text, re.IGNORECASE | re.DOTALL)
    if ref_match:
        ref_lines = ref_match.group(1).strip().split('\n')
        # Clean up bullet points or numbers from the start of the line
        cleaned_refs = [re.sub(r'^[\d\.\-\*]+\s*', '', line.strip()) for line in ref_lines if line.strip()]
        sections['references'] = cleaned_refs
        
    # 4. Extract Body (everything that starts with a single # and isn't a special tag)
    # We remove the @ABSTRACT, @KEYWORDS, @REFERENCES blocks to leave just the body.
    body_text = text
    body_text = re.sub(r'@ABSTRACT\s*\n.*?(?=\n@|\n#|$)', '', body_text, flags=re.IGNORECASE | re.DOTALL)
    body_text = re.sub(r'@KEYWORDS\s*\n.*?(?=\n@|\n#|$)', '', body_text, flags=re.IGNORECASE | re.DOTALL)
    body_text = re.sub(r'@REFERENCES\s*\n.*?(?=\n@|\n#|$)', '', body_text, flags=re.IGNORECASE | re.DOTALL)
    
    sections['body'] = body_text.strip()
    return sections

def escape_latex(text):
    """Escapes special LaTeX characters in regular text."""
    text = text.replace('\\', r'\textbackslash{}')
    text = text.replace('%', r'\%')
    text = text.replace('#', r'\#')
    text = text.replace('_', r'\_')
    text = text.replace('{', r'\{')
    text = text.replace('}', r'\}')
    text = text.replace('&', r'\&')
    return text

def convert_markdown_to_latex(text):
    """Convert basic markdown elements to LaTeX."""
    # First, handle equations to avoid escaping their special characters
    equations = []
    def save_equation(match):
        equations.append(match.group(1))
        return f"__EQUATION_{len(equations)-1}__"
    
    inline_equations = []
    def save_inline_equation(match):
        inline_equations.append(match.group(1))
        return f"__INLINE_EQUATION_{len(inline_equations)-1}__"
        
    # Block equations $$...$$
    text = re.sub(r'\$\$(.*?)\$\$', save_equation, text, flags=re.DOTALL)
    # Inline equations $...$
    text = re.sub(r'(?<!\$)\$(?!\$)(.*?)(?<!\$)\$(?!\$)', save_inline_equation, text)
    
    import os
    # Handle Images ![caption](path) BEFORE escaping
    images = []
    def save_image(match):
        path = match.group(2)
        filename = os.path.basename(path)
        name_only, _ = os.path.splitext(filename)
        # Formulate caption from the image file name
        caption = name_only.replace('_', ' ').replace('-', ' ').title()
        # Direct it to the 'image' folder
        local_path = f"image/{filename}"
        images.append((caption, local_path))
        return f"__IMAGE_{len(images)-1}__"
    text = re.sub(r'!\[([^\]]+)\]\(([^)]+)\)', save_image, text)
    
    # Handle Sections (# Section, ## Subsection)
    text = re.sub(r'^#\s+(.*?)$', r'\\section{\1}', text, flags=re.MULTILINE)
    text = re.sub(r'^##\s+(.*?)$', r'\\subsection{\1}', text, flags=re.MULTILINE)

    # Convert bold and italics
    text = re.sub(r'\*\*(.*?)\*\*', r'\\textbf{\1}', text)
    text = re.sub(r'(?<!\*)\*(?!\*)(.*?)(?<!\*)\*(?!\*)', r'\\textit{\1}', text)
    
    # The text still has some unescaped markdown stuff that we could escape, but for now
    # equations, sections, and images are protected by placeholder strings or already converted to latex.
    # Note: escaping here would break the \section{} we just inserted, so we'll just leave escaping out 
    # of this specific block to avoid complex parsing. If we wanted strict escaping, we should parse 
    # into an AST, but regex replacements work for now if the user follows the rules.
    # Since we need to escape normal text, let's just do a naive replace of % and & which are common culprits.
    text = text.replace('%', r'\%')
    text = text.replace('&', r'\&')
    
    # Restore block equations
    for i, eq in enumerate(equations):
        clean_eq = eq.strip()
        text = text.replace(f"__EQUATION_{i}__", f"\n\\begin{{equation}}\n\\resizebox{{0.89\\columnwidth}}{{!}}{{$\\displaystyle {clean_eq}$}}\n\\end{{equation}}\n")
        
    # Restore inline equations
    for i, eq in enumerate(inline_equations):
        text = text.replace(f"__INLINE_EQUATION_{i}__", f"${eq}$")
        
    # Restore images
    for i, (caption, path) in enumerate(images):
        latex_img = (
            f"\n\\begin{{figure}}[htbp]\n"
            f"\\centerline{{\\includegraphics[width=\\linewidth]{{{path}}}}}\n"
            f"\\caption{{{escape_latex(caption)}}}\n"
            f"\\label{{fig_{i}}}\n"
            f"\\end{{figure}}\n"
        )
        text = text.replace(f"__IMAGE_{i}__", latex_img)
    
    # Split by paragraphs (double newlines) and ensure blank lines between them in LaTeX
    paragraphs = text.split('\n\n')
    text = '\n\n'.join(p.strip() for p in paragraphs if p.strip())
    
    return text

def inject_into_template(template_text, sections):
    """Injects extracted sections into the IEEE template."""
    out_text = template_text
    
    # 1. Replace Abstract
    if sections['abstract']:
        # Only escape simple things for abstract
        abs_text = sections['abstract'].replace('%', r'\%').replace('&', r'\&')
        # We find \begin{abstract} and \end{abstract} and replace everything in between.
        out_text = re.sub(
            r'(\\begin\{abstract\}).*?(\\end\{abstract\})',
            lambda m: f"{m.group(1)}\n{abs_text}\n{m.group(2)}",
            out_text,
            flags=re.DOTALL
        )
        
    # 2. Replace Keywords
    if sections['keywords']:
        kw_text = sections['keywords'].replace('%', r'\%').replace('&', r'\&')
        out_text = re.sub(
            r'(\\begin\{IEEEkeywords\}).*?(\\end\{IEEEkeywords\})',
            lambda m: f"{m.group(1)}\n{kw_text}\n{m.group(2)}",
            out_text,
            flags=re.DOTALL
        )
        
    # 3. Replace the Body
    if sections['body']:
        body_text = convert_markdown_to_latex(sections['body'])
        
        # Replace everything between the keywords (or abstract if no keywords) and References
        # We find \section{Introduction} in the template as the injection point.
        # We wipe out the template's example body up to \begin{thebibliography}
        body_replacement = body_text + '\n\n'
        
        out_text = re.sub(
            r'\\section\{Introduction\}.*?(?=\\begin\{thebibliography\})',
            lambda m: body_replacement,
            out_text,
            flags=re.DOTALL
        )
        
    # 4. Replace References
    if sections['references']:
        bib_items = ""
        for i, ref in enumerate(sections['references'], 1):
            clean_ref = ref.replace('%', r'\%').replace('&', r'\&')
            bib_items += f"\\bibitem{{b{i}}} {clean_ref}\n"
            
        bib_replacement = f"\\begin{{thebibliography}}{{00}}\n{bib_items}\\end{{thebibliography}}"
        
        out_text = re.sub(
            r'\\begin\{thebibliography\}(.*?)\\end\{thebibliography\}',
            lambda m: bib_replacement,
            out_text,
            flags=re.DOTALL
        )
        
    return out_text

def main():
    print("Reading files...")
    if not os.path.exists("output.txt"):
        print("Error: output.txt not found.")
        return
        
    if not os.path.exists("template.tex"):
        print("Error: template.tex not found.")
        return

    text = read_file("output.txt")
    template = read_file("template.tex")
    
    print("Extracting sections...")
    sections = extract_sections(text)
    
    print("Injecting into LaTeX template...")
    final_latex = inject_into_template(template, sections)
    
    write_file("final_paper.tex", final_latex)
    print("Successfully generated final_paper.tex")
    
    print("Compiling PDF with pdflatex...")
    try:
        import subprocess
        import shutil
        
        # Determine pdflatex path
        pdflatex_path = shutil.which('pdflatex')
        if not pdflatex_path:
            # Fallback path for standard MiKTeX installation via winget
            fallback = r"C:\Users\Ronit\AppData\Local\Programs\MiKTeX\miktex\bin\x64\pdflatex.exe"
            if os.path.exists(fallback):
                pdflatex_path = fallback
            else:
                raise FileNotFoundError("pdflatex not found in PATH or standard installation directory.")
                
        # Run pdflatex non-interactively
        result = subprocess.run(
            [pdflatex_path, '-interaction=nonstopmode', 'final_paper.tex'],
            cwd=os.getcwd(),
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            print("Successfully compiled final_paper.pdf")
        else:
            print("PDF compilation failed with errors. Check final_paper.log")
            # print(result.stdout) # Un-comment to debug LaTeX errors
    except FileNotFoundError as e:
        print(e)
    except Exception as e:
        print(f"Error compiling PDF: {e}")

if __name__ == "__main__":
    main()
