# intel_Unnati_MIT
This project is a business contract classification tool designed to extract text from PDF files, compare clauses within the documents, classify the clauses, and generate a report highlighting the differences. It uses `pdfplumber` for text extraction and `difflib` for comparing text. The classification and prediction of clause types are done using a `BERT`-based model implemented with PyTorch. The front-end is developed in `React`, and the back-end is powered by `Flask`.

## Features

- Extract text from PDF files uploaded.
- Identify and parse clauses from the extracted text.
- Compare clauses from two different PDF documents.
- Generate a report highlighting the differences between the clauses.
- Make a PDF with the deviations highlighted

## Installation

1. Clone the repository:
   ```sh
   git clone https://github.com/saisudan2003/intel_Unnati_MIT.git
   cd intel_Unnati_MIT
   pip install -r requirements.txt
   ```

2. To run the front-end:
   ```
   cd frontend
   npm dev
   ```
3. To run the python app:
   ```
   cd ..
   python app.py
   ```

## Project Demo - Video Link

The following is a video link showing the working of our solution.
https://drive.google.com/file/d/1Jk2WTyZikz67j6IhInnmo3tsekZYTA0s/view?usp=sharing

## Data Folder

The following is the drive link to the data folder we used for training the model.
https://drive.google.com/drive/folders/1LHpsZnK7DVCcpGwTVArYcSTKWIYY0jQj?usp=sharing

1. The 'raw' folder contains the raw legal agreement PDFs obtained by us.
2. The 'processed' folder contains the raw PDFs converted to textual format by our parser.
3. The 'annotated' folder contains the processed texts annotated into clauses through classification.

## Project Structure

intel_Unnati_MIT/
├── input_folder/
│   ├── example/
│   │   └── example.pdf `The sample PDF uploaded by the user`
│   │   └── example.txt `The sample after preprocessing and parsing into textual format (Appears after running pdf-parser)`
│   ├── template/
│   │   └── template.pdf `The template PDF uploaded by the user`
│   │   └── template.txt `The template after preprocessing and parsing into textual format(Appears after running pdf-parser)`
├── src/
│   ├── classification/
│   │   └── annotate_files_v3.py `Annotates the processed texts into clauses of partciular type using the model`
│   │   └── compare_clauses.py `Compares the clauses in the processed sample document and tempate document using regex`
│   │   └── preprocess.py `Preprocesses the PDFs to make it in a form readable by the model`
│   │   └── train_model_v2.py `Trains the machine learning model using BERT`
│   │   └── highlight_differences.py `Highlights the deviations detected in the sample PDF and creates a new PDF`
│   ├── parsing/
│   │   └── pdf-parser.py `Parses the PDFs uploaded into textual format`
├── reports/
│   └── inconsistencies_report.txt `Deviations detected in a textual report format(Appears after running compare_clauses)`
├── main.py
├── requirements.txt
└── README.md

## Sample data used in the Project Demo Video

Input template pdf:
https://drive.google.com/file/d/1IG9przvvuzbQ3u5XCJTHWGzlre1auWxE/view

Input sample pdf:
https://drive.google.com/file/d/1udbQcRVp_Pwku-3tZcfW1HDjgHjdmt6s/view

## Conclusion

This model works fine with most templates and sample PDF documents. Unfortunately, due to limited availability of training dataset for our machine learning model, it is not very accurate. Hence we are using Regex to extract clauses and compare them. We hope to improve upon this in our next iteration. 

## PPT

Attached below is a powerpoint presentation of our project.
https://docs.google.com/presentation/d/1E0SVlbnPuNOBBa2iZsYEsP9FNI6_A8iI/edit?usp=sharing&ouid=104593993575231786636&rtpof=true&sd=true
