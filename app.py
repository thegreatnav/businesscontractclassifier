import os
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
from flask_cors import CORS

from src.classification.preprocess import process_pdfs
from src.classification.annotate_files_v3 import annotate_files
from src.classification.compare_clauses import load_classified_file, compare_clauses, generate_report
import torch
from transformers import BertForSequenceClassification, BertTokenizer

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
app.config['UPLOAD_FOLDER'] = 'input_folder'

# Load the trained model and tokenizer
model_path = "src/classification/contract_classifier_v2"
model = BertForSequenceClassification.from_pretrained(model_path)
tokenizer = BertTokenizer.from_pretrained(model_path)

def save_uploaded_file(file, folder):
    filename = secure_filename(file.filename)
    file_path = os.path.join(folder, filename)
    file.save(file_path)
    return file_path

def clear_input_folder():
    for folder_name in ['template', 'example', 'processed/template', 'processed/example', 'classified/template', 'classified/example', 'reports']:
        folder_path = os.path.join(app.config['UPLOAD_FOLDER'], folder_name)
        for file in os.listdir(folder_path):
            file_path = os.path.join(folder_path, file)
            if os.path.isfile(file_path):
                os.remove(file_path)

@app.route('/process', methods=['POST'])
def process_files():
    if 'template' not in request.files or 'example' not in request.files:
        return jsonify({'error': 'Template and Example files are required'}), 400

    template_file = request.files['template']
    example_file = request.files['example']

    template_pdf_path = save_uploaded_file(template_file, os.path.join(app.config['UPLOAD_FOLDER'], 'template'))
    example_pdf_path = save_uploaded_file(example_file, os.path.join(app.config['UPLOAD_FOLDER'], 'example'))

    # Process PDFs to extract text
    process_pdfs(os.path.join(app.config['UPLOAD_FOLDER'], 'template'), os.path.join(app.config['UPLOAD_FOLDER'], 'processed/template'))
    process_pdfs(os.path.join(app.config['UPLOAD_FOLDER'], 'example'), os.path.join(app.config['UPLOAD_FOLDER'], 'processed/example'))

    # Annotate files
    annotate_files(model, tokenizer, os.path.join(app.config['UPLOAD_FOLDER'], 'processed/template'), os.path.join(app.config['UPLOAD_FOLDER'], 'classified/template'))
    annotate_files(model, tokenizer, os.path.join(app.config['UPLOAD_FOLDER'], 'processed/example'), os.path.join(app.config['UPLOAD_FOLDER'], 'classified/example'))

    # Compare files
    template_file = os.path.join(app.config['UPLOAD_FOLDER'], 'classified/template/template.txt')
    example_file = os.path.join(app.config['UPLOAD_FOLDER'], 'classified/example/example.txt')
    output_file = os.path.join(app.config['UPLOAD_FOLDER'], 'reports/inconsistencies_report.txt')

    template_clauses = load_classified_file(template_file)
    example_clauses = load_classified_file(example_file)
    differences = compare_clauses(template_clauses, example_clauses)

    generate_report(differences, output_file)

    # Read the report
    with open(output_file, "r") as report_file:
        report_content = report_file.read()

    # Clear input folder
    clear_input_folder()

    return jsonify({'report': report_content}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)

