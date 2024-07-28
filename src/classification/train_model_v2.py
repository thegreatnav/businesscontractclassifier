import os
import json
import torch
from transformers import BertForSequenceClassification, BertTokenizer, AdamW, get_linear_schedule_with_warmup

def load_data(file_path):
    with open(file_path, "r") as file:
        data = json.load(file)
    texts = [item['text'] for item in data]
    labels = [item['clause_type'] for item in data]
    return texts, labels

def preprocess_data(texts, labels, tokenizer, max_length=512):
    encodings = tokenizer(texts, truncation=True, padding=True, max_length=max_length, return_tensors='pt')
    return encodings, labels

if __name__ == "__main__":
    # Load the dataset
    texts, labels = load_data("data/processed/combined_annotated_data.json")

    # Convert labels to integers
    label_set = list(set(labels))
    label_to_id = {label: i for i, label in enumerate(label_set)}
    labels = [label_to_id[label] for label in labels]

    # Split data into train and test
    split_idx = int(0.8 * len(texts))
    train_texts, test_texts = texts[:split_idx], texts[split_idx:]
    train_labels, test_labels = labels[:split_idx], labels[split_idx:]

    # Load the tokenizer and model
    tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
    model = BertForSequenceClassification.from_pretrained('bert-base-uncased', num_labels=len(label_set))

    # Preprocess the data
    train_encodings, train_labels = preprocess_data(train_texts, train_labels, tokenizer)
    test_encodings, test_labels = preprocess_data(test_texts, test_labels, tokenizer)

    # Create the data loaders
    train_dataset = torch.utils.data.TensorDataset(train_encodings['input_ids'], train_encodings['attention_mask'], torch.tensor(train_labels))
    test_dataset = torch.utils.data.TensorDataset(test_encodings['input_ids'], test_encodings['attention_mask'], torch.tensor(test_labels))
    
    train_loader = torch.utils.data.DataLoader(train_dataset, batch_size=8, shuffle=True)
    test_loader = torch.utils.data.DataLoader(test_dataset, batch_size=8, shuffle=False)

    # Move model to GPU
    device = torch.device("mps" if torch.backends.mps.is_available() else "cpu")
    model.to(device)

    # Define optimizer and scheduler
    optimizer = AdamW(model.parameters(), lr=2e-5)
    total_steps = len(train_loader) * 3  # Number of training steps
    scheduler = get_linear_schedule_with_warmup(optimizer, num_warmup_steps=0, num_training_steps=total_steps)

    # Define training loop
    def train():
        model.train()
        for epoch in range(3):
            for batch in train_loader:
                b_input_ids, b_attention_mask, b_labels = [x.to(device) for x in batch]
                optimizer.zero_grad()
                outputs = model(input_ids=b_input_ids, attention_mask=b_attention_mask, labels=b_labels)
                loss = outputs.loss
                loss.backward()
                optimizer.step()
                scheduler.step()
            print(f"Epoch {epoch + 1} completed.")

    # Train the model
    train()

    # Save the model
    model.save_pretrained("src/classification/contract_classifier_v2")
    tokenizer.save_pretrained("src/classification/contract_classifier_v2")
