import pdfplumber
import os

def extract_text_from_pdf(pdf_path, txt_path):
    with pdfplumber.open(pdf_path) as pdf:
        text = ""
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text
                text += "\n\n"  # Ensure each page ends with two newlines for separation

    with open(txt_path, "w") as text_file:
        text_file.write(text)

def process_pdfs(input_dir, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    for pdf_file in os.listdir(input_dir):
        if pdf_file.endswith(".pdf"):
            pdf_path = os.path.join(input_dir, pdf_file)
            txt_path = os.path.join(output_dir, pdf_file.replace(".pdf", ".txt"))
            extract_text_from_pdf(pdf_path, txt_path)

if __name__ == "__main__":
    process_pdfs("input_folder/template", "input_folder/processed/template")
    process_pdfs("input_folder/example", "input_folder/processed/example")