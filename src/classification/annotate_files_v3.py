import os
import torch
from transformers import BertForSequenceClassification, BertTokenizer
import re

# Load the trained model and tokenizer
model_path = "src/classification/contract_classifier_v2"
model = BertForSequenceClassification.from_pretrained(model_path)
tokenizer = BertTokenizer.from_pretrained(model_path)

def extract_clauses(text):
    # Define regex patterns for clause identification
    clause_patterns = [
        r'(Section \d+\. [A-Za-z ]+)',  # Match "Section 1. Clause Title"
        r'([a-z]\.\s)',  # Match "a. "
        r'(\d\.\s)',     # Match "1. "
        r'([A-Za-z]+\.)' # Match "Title."
    ]

    # Split text into potential clauses based on patterns
    clauses = []
    current_clause = ""
    for line in text.split("\n"):
        line = line.strip()
        if line:
            is_new_clause = any(re.match(pattern, line) for pattern in clause_patterns)
            if is_new_clause and current_clause:  # Start a new clause if a new clause pattern is detected
                clauses.append(current_clause.strip())
                current_clause = line
            else:
                current_clause += "\n" + line
        else:
            if current_clause:
                clauses.append(current_clause.strip())
                current_clause = ""
    if current_clause:
        clauses.append(current_clause.strip())
    return clauses

def predict_annotations(model, tokenizer, text):
    inputs = tokenizer(text, return_tensors='pt', truncation=True, padding=True)
    outputs = model(**inputs)
    predictions = torch.argmax(outputs.logits, dim=1)
    return predictions

def annotate_files(model, tokenizer, input_dir, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    for text_file in os.listdir(input_dir):
        if text_file.endswith(".txt"):
            file_path = os.path.join(input_dir, text_file)
            with open(file_path, "r") as file:
                text = file.read()
                clauses = extract_clauses(text)
                annotated_text = ""
                clause_id = 1
                for clause in clauses:
                    # predictions = predict_annotations(model, tokenizer, clause)
                    annotated_text += f"<CLAUSE:{clause_id}>\n{clause}\n</CLAUSE:{clause_id}>\n"
                    clause_id += 1
                output_path = os.path.join(output_dir, text_file)
                with open(output_path, "w") as annotated_file:
                    annotated_file.write(annotated_text)

if __name__ == "__main__":
    annotate_files(model, tokenizer, "input_folder/processed/template", "input_folder/classified/template")
    annotate_files(model, tokenizer, "input_folder/processed/example", "input_folder/classified/example")
