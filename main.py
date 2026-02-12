# main.py
import os
import pandas as pd
from datetime import datetime
from extractors.pdf_parser import TextPDFExtractor, ScannedPDFExtractor
from extractors.table_extractor import TableExtractor
from utils.file_handler import FileHandler

class PDFDataExtractor:
    def __init__(self):
        self.text_extractor = TextPDFExtractor()
        self.scanned_extractor = ScannedPDFExtractor()
        self.table_extractor = TableExtractor()
        self.file_handler = FileHandler()
    
    def process_pdf(self, pdf_path, pdf_type='text', extraction_type='tables'):
        """Process single PDF"""
        print(f"\n📄 Processing: {os.path.basename(pdf_path)}")
        
        results = []
        
        try:
            if extraction_type == 'tables':
                # Extract tables
                if pdf_type == 'text':
                    tables = self.text_extractor.extract_tables(pdf_path)
                else:
                    tables = self.scanned_extractor.extract_tables_from_scanned(pdf_path)
                
                # Save tables
                if tables:
                    output_file = self.file_handler.get_output_path(pdf_path)
                    self.table_extractor.save_to_excel(tables, output_file)
                    results.append({'file': pdf_path, 'status': 'success', 'tables': len(tables)})
                
            elif extraction_type == 'invoice':
                # Extract invoice fields
                data = self.text_extractor.extract_invoice_data(pdf_path)
                if data:
                    df = pd.DataFrame(data)
                    output_file = self.file_handler.get_output_path(pdf_path, suffix='_invoice')
                    df.to_excel(output_file, index=False)
                    results.append({'file': pdf_path, 'status': 'success'})
            
            # Move processed file
            self.file_handler.move_processed(pdf_path)
            
        except Exception as e:
            print(f"❌ Error: {e}")
            results.append({'file': pdf_path, 'status': 'failed', 'error': str(e)})
        
        return results
    
    def process_folder(self, folder_path='pdfs', pdf_type='text', extraction_type='tables'):
        """Process all PDFs in folder"""
        pdf_files = self.file_handler.get_pdf_files(folder_path)
        
        if not pdf_files:
            print("❌ No PDF files found in 'pdfs' folder")
            return
        
        print(f"📊 Found {len(pdf_files)} PDF files to process")
        
        all_results = []
        for pdf_file in pdf_files:
            result = self.process_pdf(pdf_file, pdf_type, extraction_type)
            all_results.extend(result)
        
        # Save summary report
        summary_df = pd.DataFrame(all_results)
        summary_file = f"output/summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        summary_df.to_csv(summary_file, index=False)
        
        print(f"\n✅ Processing complete!")
        print(f"📁 Output saved to: output/")
        print(f"📊 Summary: {summary_file}")
        
        return all_results

def main():
    print("="*60)
    print("📄 PDF DATA EXTRACTOR")
    print("="*60)
    
    # Create necessary folders
    os.makedirs('pdfs', exist_ok=True)
    os.makedirs('output', exist_ok=True)
    os.makedirs('processed', exist_ok=True)
    
    # Configuration
    print("\n🔧 Configuration:")
    print("1. PDF Type:")
    print("   - text: Normal PDFs (selectable text)")
    print("   - scanned: Scanned PDFs (need OCR)")
    
    pdf_type = input("\nPDF Type (text/scanned): ").strip().lower() or 'text'
    
    print("\n2. Extraction Type:")
    print("   - tables: Extract tables from PDF")
    print("   - invoice: Extract invoice fields")
    print("   - custom: Custom regex patterns")
    
    extraction_type = input("Extraction Type (tables/invoice/custom): ").strip().lower() or 'tables'
    
    # Run extraction
    extractor = PDFDataExtractor()
    results = extractor.process_folder(
        folder_path='pdfs',
        pdf_type=pdf_type,
        extraction_type=extraction_type
    )
    
    # Summary
    success = len([r for r in results if r['status'] == 'success'])
    failed = len([r for r in results if r['status'] == 'failed'])
    
    print(f"\n📊 FINAL SUMMARY:")
    print(f"   ✅ Success: {success}")
    print(f"   ❌ Failed: {failed}")
    print(f"   📁 Check output folder for Excel files")

if __name__ == "__main__":
    main()