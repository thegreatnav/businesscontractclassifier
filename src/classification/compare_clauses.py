import difflib
import fitz  # PyMuPDF
import logging
import re

# Set up logging
logging.basicConfig(filename='debug.log', level=logging.DEBUG, format='%(asctime)s %(message)s')

def load_classified_file(file_path):
    with open(file_path, "r") as file:
        data = file.read().strip().split("<CLAUSE:")
    clauses = {}
    for clause in data:
        if clause.strip():
            clause_id, clause_text = clause.split(">", 1)
            clauses[clause_id.strip()] = clause_text.strip()
    logging.debug(f"Loaded {len(clauses)} clauses from {file_path}")
    return clauses

def normalize_text(text):
    # Normalize whitespace characters for more meaningful comparison
    return ' '.join(text.split())

def remove_clause_tags(text):
    # Remove the </CLAUSE:> tags from the text
    return re.sub(r'</CLAUSE:\d+>', '', text).strip()

def compare_clauses(template_clauses, example_clauses):
    differences = []
    all_keys = set(template_clauses.keys()).union(set(example_clauses.keys()))
    
    for key in all_keys:
        template_clause = template_clauses.get(key, "")
        example_clause = example_clauses.get(key, "")
        
        normalized_template_clause = normalize_text(template_clause)
        normalized_example_clause = normalize_text(example_clause)
        
        if normalized_template_clause != normalized_example_clause:
            diff = '\n'.join(difflib.unified_diff(
                template_clause.splitlines(),
                example_clause.splitlines(),
                fromfile=f'Template Clause {key}',
                tofile=f'Example Clause {key}',
                lineterm=''
            ))
            differences.append({
                "template_clause": remove_clause_tags(template_clause),
                "example_clause": remove_clause_tags(example_clause),
                "diff": diff,
                "clause_id": key
            })
            logging.debug(f"Differences found in clause {key}")
    
    return differences

def generate_report(differences, output_file):
    with open(output_file, "w") as file:
        for i, diff in enumerate(differences, 1):
            file.write(f"----------------------\n")
            file.write(f"template inconsistency {i}:\n")
            file.write(diff["template_clause"] + "\n")
            file.write(f"example inconsistency {i}:\n")
            file.write(diff["example_clause"] + "\n")
            file.write(f"----------------------\n")

def highlight_inconsistencies_in_pdf(differences, example_pdf_path, output_pdf_path):
    doc = fitz.open(example_pdf_path)
    for diff in differences:
        example_clause = diff["example_clause"]
        template_clause = diff["template_clause"]
        normalized_example_clause = normalize_text(example_clause)
        normalized_template_clause = normalize_text(template_clause)
        
        for page_num in range(len(doc)):
            page = doc[page_num]
            
            # Search for the exact example clause first
            text_instances = page.search_for(example_clause)
            # Fallback to normalized example clause if exact match fails
            if not text_instances:
                text_instances = page.search_for(normalized_example_clause)
            # Fallback to template clause if exact match fails
            if not text_instances:
                text_instances = page.search_for(template_clause)
            # Further fallback to searching the normalized template clause
            if not text_instances:
                text_instances = page.search_for(normalized_template_clause)
            
            if text_instances:
                logging.debug(f"Found {len(text_instances)} instances on page {page_num}")
                for inst in text_instances:
                    highlight = page.add_highlight_annot(inst)
                    highlight.set_colors({"stroke": (1, 0, 0), "fill": (1, 1, 0)})  # Red stroke, yellow fill
                    highlight.update()
    doc.save(output_pdf_path)
    logging.debug(f"Highlighted PDF saved to {output_pdf_path}")

if __name__ == "__main__":
    template_file = "input_folder/classified/template/template.txt"
    example_file = "input_folder/classified/example/example.txt"
    example_pdf_path = "input_folder/example/example.pdf"
    output_file = "input_folder/reports/inconsistencies_report.txt"
    output_pdf_path = "input_folder/reports/highlighted_inconsistencies.pdf"
    
    template_clauses = load_classified_file(template_file)
    example_clauses = load_classified_file(example_file)
    differences = compare_clauses(template_clauses, example_clauses)
    
    generate_report(differences, output_file)
    highlight_inconsistencies_in_pdf(differences, example_pdf_path, output_pdf_path)
    
    logging.debug("Comparison complete, report and highlighted PDF generated.")
