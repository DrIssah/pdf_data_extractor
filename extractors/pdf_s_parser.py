# extractors/pdf_parser.py - For SCANNED PDFs
import fitz  # PyMuPDF
import pytesseract
from PIL import Image
import io
import pandas as pd
import os

class ScannedPDFExtractor:
    def __init__(self):
        # Point to tesseract.exe (Windows)
        pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    
    def extract_text_from_scanned_pdf(self, pdf_path):
        """Extract text from scanned PDF using OCR"""
        doc = fitz.open(pdf_path)
        all_text = []
        
        for page_num in range(len(doc)):
            page = doc[page_num]
            
            # Convert PDF page to image
            pix = page.get_pixmap(matrix=fitz.Matrix(300/72, 300/72))
            img_data = pix.tobytes("png")
            img = Image.open(io.BytesIO(img_data))
            
            # OCR with English language
            text = pytesseract.image_to_string(img, lang='eng')
            all_text.append(text)
            
        doc.close()
        return '\n'.join(all_text)
    
    def extract_tables_from_scanned(self, pdf_path):
        """Try to detect tables in scanned PDFs"""
        doc = fitz.open(pdf_path)
        all_tables = []
        
        for page_num in range(len(doc)):
            page = doc[page_num]
            
            # Find table areas (look for lines/boxes)
            pix = page.get_pixmap(matrix=fitz.Matrix(300/72, 300/72))
            img_data = pix.tobytes("png")
            img = Image.open(io.BytesIO(img_data))
            
            # Use Tesseract with table detection
            data = pytesseract.image_to_data(img, output_type=pytesseract.Output.DICT)
            
            # Group text into rows/columns (simplified)
            rows = {}
            for i, text in enumerate(data['text']):
                if text.strip():
                    left = data['left'][i]
                    top = data['top'][i]
                    row_key = round(top / 20)  # Group by vertical position
                    
                    if row_key not in rows:
                        rows[row_key] = []
                    rows[row_key].append((left, text))
            
            # Sort each row by left position
            table_data = []
            for row_key in sorted(rows.keys()):
                row_text = [text for _, text in sorted(rows[row_key])]
                table_data.append(row_text)
            
            all_tables.extend(table_data)
        
        doc.close()
        return all_tables