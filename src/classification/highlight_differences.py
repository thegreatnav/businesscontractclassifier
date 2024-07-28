import fitz  # PyMuPDF
import re

# Function to parse the differences report
def parse_differences_report(report):
    template_clause = re.search(r'template clause:\n(.+)', report).group(1)
    example_clause = re.search(r'example clause:\n(.+)', report).group(1)
    differences = re.findall(r'@@.*\n-(.*)\n\+(.*)', report)
    #print(differences)
    return template_clause, example_clause, differences

def merge_sentences(text):
    """Merge lines that are part of the same sentence."""
    lines = text.split('\n')
    merged_lines = []
    current_line = ''

    for line in lines:
        stripped_line = line.strip()
        if not stripped_line:
            # Empty line indicates paragraph break
            if current_line:
                merged_lines.append(current_line.strip())
                current_line = ''
            merged_lines.append('')
        elif re.match(r'^[A-Z].*[.!?]\s*$', stripped_line):
            # Line starts with uppercase letter and ends with sentence-ending punctuation
            current_line += ' ' + stripped_line
            merged_lines.append(current_line.strip())
            current_line = ''
        else:
            # Line is part of the same sentence
            current_line += ' ' + stripped_line

    if current_line:
        merged_lines.append(current_line.strip())

    return '\n'.join(merged_lines)

# Function to highlight differences and add pop-up notes in a PDF
def highlight_differences(pdf_path, output_path, differences):
    # Open the PDF
    doc = fitz.open(pdf_path)
    
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        text = page.get_text("text")
        merged_text = merge_sentences(text)
        cleaned_text = re.sub(r'\n+', '\n', merged_text).strip()
        #print(cleaned_text)

        for old, new in differences:
            if new in cleaned_text:
                areas = page.search_for(new)
                for area in areas:
                    highlight = page.add_highlight_annot(area)
                    note = f"Expected: {old}\nFound: {new}"
                    # Create a very small invisible annotation near the text
                    rect = fitz.Rect(area.br.x - 1, area.br.y - 1, area.br.x, area.br.y)
                    popup = page.add_freetext_annot(rect, note, fontsize=1, text_color=(0, 0, 0), fill_color=(1, 1, 1), border_color=(1, 1, 1))
                    highlight.set_popup(popup)

            """if old in text:
                areas = page.search_for(old)
                for area in areas:
                    highlight = page.add_highlight_annot(area)
                    note = f"Expected: {old}\nFound: {new}"
                    # Create a very small invisible annotation near the text
                    rect = fitz.Rect(area.br.x - 1, area.br.y - 1, area.br.x, area.br.y)
                    popup = page.add_freetext_annot(rect, note, fontsize=1, text_color=(0, 0, 0), fill_color=(1, 1, 1), border_color=(1, 1, 1))
                    highlight.set_popup(popup)"""
    
    # Save the new PDF
    doc.save(output_path)

# Example usage
report_file_path = "C:/Users/91949/Downloads/intel_unnati/intel_unnati_updt/input_folder/reports/inconsistencies_report.txt"

# Read the report from a file
with open(report_file_path, "r") as file:
    report = file.read()

template_clause, example_clause, differences = parse_differences_report(report)
highlight_differences("C:/Users/91949/Downloads/intel_unnati/intel_unnati_updt/input_folder/example/example.pdf", "C:/Users/91949/Downloads/intel_unnati/intel_unnati_updt/input_folder/reports/highlighted.pdf", differences)
