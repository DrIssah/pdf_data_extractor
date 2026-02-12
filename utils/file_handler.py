import os
import shutil
from datetime import datetime

class FileHandler:
    @staticmethod
    def get_pdf_files(folder_path):
        """Get all PDF files from folder"""
        pdf_files = []
        for file in os.listdir(folder_path):
            if file.lower().endswith('.pdf'):
                pdf_files.append(os.path.join(folder_path, file))
        return pdf_files
    
    @staticmethod
    def get_output_path(pdf_path, suffix=''):
        """Generate output Excel filename"""
        base_name = os.path.basename(pdf_path)
        name_without_ext = os.path.splitext(base_name)[0]
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        return f"output/{name_without_ext}{suffix}_{timestamp}.xlsx"
    
    @staticmethod
    def move_processed(pdf_path):
        """Move processed PDF to processed folder"""
        try:
            dest = os.path.join('processed', os.path.basename(pdf_path))
            shutil.move(pdf_path, dest)
            print(f"📦 Moved to processed/")
        except:
            pass