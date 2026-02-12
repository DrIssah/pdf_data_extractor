# pdf_data_extractor
Extract data from pdfs

# 📄 PDF Text & Table Extractor

A professional Python-based tool for extracting text, tables, and structured fields from text-based PDF files.

This project is designed for automation, invoice processing, document analysis, and data extraction workflows.

---

## 🚀 Features

- ✅ Extract full text from PDF files
- ✅ Extract tables and export to Excel
- ✅ Search for specific keywords inside PDFs
- ✅ Extract structured fields (Invoice #, Date, Total, PO #)
- ✅ Batch process multiple PDFs
- ✅ Automatic folder creation
- ✅ Summary report generation
- ✅ Text caching for performance optimization
- ✅ Clean logging system

---

## 📁 Project Structure


pdf-extractor/
│
├── input_pdfs/ # Place your PDF files here
├── output_data/ # Extracted results are saved here
├── pdf_extractor.py # Main application
├── requirements.txt
└── README.md


---

## ⚙️ Installation

### 1️⃣ Clone Repository

```bash
git clone https://github.com/yourusername/pdf-extractor.git
cd pdf-extractor

2️⃣ Create Virtual Environment
python -m venv venv


Activate it:

Windows

venv\Scripts\activate


Mac/Linux

source venv/bin/activate

3️⃣ Install Dependencies
pip install -r requirements.txt

▶️ How to Run
python pdf_extractor.py


You will see a menu:

1. Process ALL PDFs
2. Search text in a PDF
3. Extract invoice fields
4. Exit

📊 Output

The program automatically creates:

📄 Extracted text files (.txt)

📊 Extracted tables (.xlsx)

📈 Summary report (.csv)

All outputs are saved inside:

output_data/

🔍 Supported PDFs

This tool works with:

✅ Text-based PDFs
❌ Scanned/image-based PDFs (OCR required for those)

🧠 Use Cases

Invoice processing automation

Financial document extraction

Academic research data extraction

Report parsing

Bulk document analysis

Data engineering preprocessing

🛠 Technologies Used

Python 3

pdfplumber

pandas

openpyxl

regex

logging

📌 Example Extracted Fields

The tool automatically extracts common invoice fields such as:

Invoice Number

Date

Total Amount

PO Number

⚠️ Limitations

Does not support scanned PDFs (OCR not implemented yet)

Table extraction depends on PDF structure

🚀 Future Improvements

Add OCR support (pytesseract)

Convert to CLI with argparse

Add multiprocessing

Create REST API version (FastAPI)

Docker containerization

Add unit tests (pytest)

📄 License

This project is open-source and free to use.

👤 Erick Yaa Yeri

Developed as part of automation and data extraction workflow projects.