import os
from pdfminer.high_level import extract_text

def parse_pdf(file_path):
    text = extract_text(file_path)
    return text

def parse_pdfs(input_dir, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    for pdf_file in os.listdir(input_dir):
        if pdf_file.endswith(".pdf"):
            pdf_path = os.path.join(input_dir, pdf_file)
            text = parse_pdf(pdf_path)
            text_file_path = os.path.join(output_dir, pdf_file.replace(".pdf", ".txt"))
            with open(text_file_path, "w") as text_file:
                text_file.write(text)

if __name__ == "__main__":
    input_dir = "data/raw/contracts"
    output_dir = "data/processed/contracts"
    parse_pdfs(input_dir, output_dir)