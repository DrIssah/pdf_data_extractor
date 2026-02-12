# extractors/pdf_parser.py - For TEXT PDFs
import pdfplumber
import pandas as pd
import re

class TextPDFExtractor:
    def extract_tables(self, pdf_path):
        """Extract tables from PDF"""
        all_tables = []
        
        with pdfplumber.open(pdf_path) as pdf:
            for page_num, page in enumerate(pdf.pages):
                # Extract tables
                tables = page.extract_tables()
                
                for table in tables:
                    if table:
                        # Convert to DataFrame
                        df = pd.DataFrame(table)
                        df = df.dropna(how='all')  # Remove empty rows
                        df = df.dropna(axis=1, how='all')  # Remove empty columns
                        
                        # Clean data
                        df = df.replace(r'\n', ' ', regex=True)
                        df = df.replace(r'\s+', ' ', regex=True)
                        
                        all_tables.append(df)
        
        return all_tables
    
    def extract_text_by_pattern(self, pdf_path, patterns):
        """Extract specific fields using regex patterns"""
        extracted_data = []
        
        with pdfplumber.open(pdf_path) as pdf:
            text = ''
            for page in pdf.pages:
                text += page.extract_text() + '\n'
            
            # Apply regex patterns
            record = {}
            for field_name, pattern in patterns.items():
                match = re.search(pattern, text)
                record[field_name] = match.group(1) if match else None
            
            extracted_data.append(record)
        
        return extracted_data
    
    def extract_invoice_data(self, pdf_path):
        """Example: Extract specific invoice fields"""
        patterns = {
            'invoice_number': r'Invoice #?\s*:?\s*([A-Z0-9-]+)',
            'date': r'Date\s*:?\s*(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})',
            'total': r'Total\s*:?\s*\$?([0-9,]+\.?\d*)',
            'customer': r'Bill To\s*:?\s*([^\n]+)',
            'po_number': r'PO #?\s*:?\s*([A-Z0-9-]+)',
        }
        return self.extract_text_by_pattern(pdf_path, patterns)