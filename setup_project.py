import os
import re

TEX_TEMPLATE = "template.tex"
PROMPT_TEMPLATE = "prompt.txt"
GENERATED_PROMPT = "generated_prompt.txt"

def update_title_and_authors():
    print("=== Step 1: Paper Title Configuration ===")
    title = input("What is the title of the paper? ")
    
    print("\n=== Step 2: Author Configuration ===")
    try:
        num_authors = int(input("How many authors are there? "))
    except ValueError:
        print("Invalid number. Defaulting to 1.")
        num_authors = 1
        
    authors_latex = []
    
    for i in range(1, num_authors + 1):
        print(f"\n--- Author {i} ---")
        name = input("Full Name: ")
        dept = input("Department (e.g. Dept. of Computer Science): ")
        org = input("Organization/University: ")
        city_country = input("City, Country: ")
        email = input("Email or ORCID: ")
        
        # Determine ordinal suffix
        if i == 1: suffix = "st"
        elif i == 2: suffix = "nd"
        elif i == 3: suffix = "rd"
        else: suffix = "th"
            
        author_block = f"""\\IEEEauthorblockN{{{i}\\textsuperscript{{{suffix}}} {name}}}
\\IEEEauthorblockA{{\\textit{{{dept}}} \\\\
\\textit{{{org}}}\\\\
{city_country} \\\\
{email}}}"""
        authors_latex.append(author_block)
        
    author_str = "\\author{" + "\n\\and\n".join(authors_latex) + "\n}"
    
    print("\nUpdating template.tex...")
    if os.path.exists(TEX_TEMPLATE):
        with open(TEX_TEMPLATE, "r", encoding="utf-8") as f:
            template = f.read()
            
        # First replace the \title{...} block up to \author
        new_template = re.sub(
            r'\\title\{.*?\}\s*(?=\\author\{)',
            lambda m: f"\\title{{{title}}}\n\n",
            template,
            flags=re.DOTALL
        )

        # Then replace the \author{...} block up to \maketitle
        new_template = re.sub(
            r'\\author\{.*?\}\s*(?=\\maketitle)',
            lambda m: author_str + '\n\n',
            new_template,
            flags=re.DOTALL
        )
        
        with open(TEX_TEMPLATE, "w", encoding="utf-8") as f:
            f.write(new_template)
        print("Done.")
    else:
        print(f"Warning: {TEX_TEMPLATE} not found!")

def update_prompt():
    print("\n=== Step 3: Paper Summary Configuration ===")
    print("Please provide the details for the LLM prompt.")
    
    topic = input("Research Topic: ")
    objective = input("Research Objective: ")
    summary = input("Paper Summary / Notes: ")
    method = input("Proposed Method / Model: ")
    dataset = input("Dataset or Experimental Context: ")
    baselines = input("Baseline Methods for Comparison: ")
    
    print("\nGenerating generated_prompt.txt...")
    if os.path.exists(PROMPT_TEMPLATE):
        with open(PROMPT_TEMPLATE, "r", encoding="utf-8") as f:
            prompt = f.read()
            
        # Replace the placeholders directly 
        prompt = prompt.replace("{RESEARCH_TOPIC}", topic)
        prompt = prompt.replace("{RESEARCH_OBJECTIVE}", objective)
        prompt = prompt.replace("{PAPER_SUMMARY}", summary)
        prompt = prompt.replace("{PROPOSED_METHOD}", method)
        prompt = prompt.replace("{DATASET_INFO}", dataset)
        prompt = prompt.replace("{BASELINE_METHODS}", baselines)
        
        with open(GENERATED_PROMPT, "w", encoding="utf-8") as f:
            f.write(prompt)
        print(f"Done. The completed prompt has been saved to {GENERATED_PROMPT}")
    else:
        print(f"Warning: {PROMPT_TEMPLATE} not found!")

if __name__ == "__main__":
    print("Welcome to the IEEE Research Paper Generator Setup!\n")
    update_title_and_authors()
    update_prompt()
    print(f"\nSetup is complete! You can now copy the text from {GENERATED_PROMPT} and pass it to the LLM.")
