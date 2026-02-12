# pdf_extractor.py

import pdfplumber
import pandas as pd
import os
import re
import logging
from datetime import datetime


# -------------------------------
# Logging Configuration
# -------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


class PDFTextExtractor:
    def __init__(self, input_folder="input_pdfs", output_folder="output_data"):
        self.input_folder = input_folder
        self.output_folder = output_folder
        self.cached_text = {}

        os.makedirs(self.input_folder, exist_ok=True)
        os.makedirs(self.output_folder, exist_ok=True)

    # -----------------------------------
    # Get PDF Files
    # -----------------------------------
    def get_pdf_files(self):
        return [
            os.path.join(self.input_folder, f)
            for f in os.listdir(self.input_folder)
            if f.lower().endswith(".pdf")
        ]

    # -----------------------------------
    # Extract Full Text (With Caching)
    # -----------------------------------
    def extract_all_text(self, pdf_path):
        if pdf_path in self.cached_text:
            return self.cached_text[pdf_path]

        full_text = ""

        try:
            with pdfplumber.open(pdf_path) as pdf:
                for page_num, page in enumerate(pdf.pages, 1):
                    text = page.extract_text()
                    if text:
                        full_text += f"\n--- PAGE {page_num} ---\n{text}\n"

            self.cached_text[pdf_path] = full_text
            return full_text

        except Exception as e:
            logging.error(f"Error reading {pdf_path}: {e}")
            return ""

    # -----------------------------------
    # Extract Tables
    # -----------------------------------
    def extract_tables(self, pdf_path):
        tables_data = []

        try:
            with pdfplumber.open(pdf_path) as pdf:
                for page_num, page in enumerate(pdf.pages, 1):
                    tables = page.extract_tables()

                    for table_num, table in enumerate(tables, 1):
                        if table and len(table) > 1:
                            df = pd.DataFrame(table[1:], columns=table[0])

                            df = df.replace(r'\n', ' ', regex=True)
                            df = df.replace(r'\s+', ' ', regex=True)
                            df = df.dropna(how='all').dropna(axis=1, how='all')

                            tables_data.append({
                                "page": page_num,
                                "table_num": table_num,
                                "dataframe": df
                            })

            return tables_data

        except Exception as e:
            logging.error(f"Error extracting tables from {pdf_path}: {e}")
            return []

    # -----------------------------------
    # Save Text
    # -----------------------------------
    def save_text(self, text, pdf_filename):
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        base = os.path.splitext(pdf_filename)[0]
        output_path = os.path.join(
            self.output_folder, f"{base}_text_{timestamp}.txt"
        )

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(text)

        return output_path

    # -----------------------------------
    # Save Tables to Excel
    # -----------------------------------
    def save_tables(self, tables, pdf_filename):
        if not tables:
            return None

        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        base = os.path.splitext(pdf_filename)[0]
        output_path = os.path.join(
            self.output_folder, f"{base}_tables_{timestamp}.xlsx"
        )

        try:
            with pd.ExcelWriter(output_path, engine="openpyxl") as writer:
                for i, table in enumerate(tables):
                    sheet_name = f"Page{table['page']}_Table{i+1}"[:31]
                    table["dataframe"].to_excel(
                        writer,
                        sheet_name=sheet_name,
                        index=False
                    )

            return output_path

        except Exception as e:
            logging.error(f"Error saving tables: {e}")
            return None

    # -----------------------------------
    # Search Text (Optimized Regex)
    # -----------------------------------
    def search_text(self, text, search_term):
        pattern = re.compile(re.escape(search_term), re.IGNORECASE)
        lines = text.split('\n')

        matches = [
            {"line_number": i + 1, "line": line.strip()}
            for i, line in enumerate(lines)
            if pattern.search(line)
        ]

        return matches

    # -----------------------------------
    # Extract Fields Using Regex Patterns
    # -----------------------------------
    def extract_fields(self, text):
        patterns = {
            "invoice_number": r'Invoice[:\s]*#?[:\s]*([A-Z0-9\-]+)',
            "date": r'Date[:\s]*([0-9]{1,2}[/\-][0-9]{1,2}[/\-][0-9]{2,4})',
            "total": r'Total[:\s]*\$?([0-9,]+\.?[0-9]*)',
            "po_number": r'PO[:\s]*#?[:\s]*([A-Z0-9\-]+)',
        }

        results = {}
        for field, pattern in patterns.items():
            match = re.search(pattern, text, re.IGNORECASE)
            results[field] = match.group(1) if match else "Not found"

        return results

    # -----------------------------------
    # Process Single PDF
    # -----------------------------------
    def process_single_pdf(self, pdf_path):
        logging.info(f"Processing: {os.path.basename(pdf_path)}")

        text = self.extract_all_text(pdf_path)
        text_file = self.save_text(text, os.path.basename(pdf_path))

        tables = self.extract_tables(pdf_path)
        excel_file = self.save_tables(tables, os.path.basename(pdf_path))

        return {
            "pdf": os.path.basename(pdf_path),
            "text_file": text_file,
            "excel_file": excel_file,
            "tables_found": len(tables),
            "text_length": len(text)
        }

    # -----------------------------------
    # Process All PDFs
    # -----------------------------------
    def process_all_pdfs(self):
        pdf_files = self.get_pdf_files()

        if not pdf_files:
            logging.warning("No PDF files found in input folder.")
            return []

        results = []

        for pdf_file in pdf_files:
            results.append(self.process_single_pdf(pdf_file))

        summary_df = pd.DataFrame(results)
        summary_file = os.path.join(
            self.output_folder,
            f"summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        )
        summary_df.to_csv(summary_file, index=False)

        logging.info("Processing complete.")
        logging.info(f"Summary saved to: {summary_file}")

        return results


# -----------------------------------
# CLI Interface
# -----------------------------------
def main():
    extractor = PDFTextExtractor()

    while True:
        print("\nPDF TEXT EXTRACTOR")
        print("1. Process ALL PDFs")
        print("2. Search text in a PDF")
        print("3. Extract invoice fields")
        print("4. Exit")

        choice = input("Choose (1-4): ").strip()

        if choice == "1":
            extractor.process_all_pdfs()

        elif choice == "2":
            pdfs = extractor.get_pdf_files()
            if not pdfs:
                print("No PDFs found.")
                continue

            for i, pdf in enumerate(pdfs, 1):
                print(f"{i}. {os.path.basename(pdf)}")

            try:
                index = int(input("Select PDF number: ")) - 1
                pdf_path = pdfs[index]
                text = extractor.extract_all_text(pdf_path)

                term = input("Enter search term: ")
                matches = extractor.search_text(text, term)

                print(f"\nFound {len(matches)} matches:")
                for m in matches[:10]:
                    print(f"Line {m['line_number']}: {m['line']}")

            except Exception:
                print("Invalid selection.")

        elif choice == "3":
            pdfs = extractor.get_pdf_files()
            if not pdfs:
                print("No PDFs found.")
                continue

            for i, pdf in enumerate(pdfs, 1):
                print(f"{i}. {os.path.basename(pdf)}")

            try:
                index = int(input("Select PDF number: ")) - 1
                pdf_path = pdfs[index]
                text = extractor.extract_all_text(pdf_path)

                fields = extractor.extract_fields(text)

                for k, v in fields.items():
                    print(f"{k}: {v}")

            except Exception:
                print("Invalid selection.")

        elif choice == "4":
            print("Goodbye.")
            break

        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()
