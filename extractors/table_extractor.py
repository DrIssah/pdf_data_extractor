# extractors/table_extractor.py
import tabula
import pandas as pd
import os

class TableExtractor:
    def extract_tables_tabula(self, pdf_path):
        """Extract tables using Tabula (BEST for tables)"""
        try:
            # Read all tables from PDF
            tables = tabula.read_pdf(
                pdf_path,
                pages='all',           # All pages
                multiple_tables=True,  # Multiple tables per page
                lattice=True,          # For bordered tables
                stream=True,           # For borderless tables
                guess=True,           # Guess table areas
                pandas_options={'header': None}
            )
            
            return tables
        except Exception as e:
            print(f"Error: {e}")
            return []
    
    def save_to_excel(self, tables, output_path):
        """Save multiple tables to Excel (different sheets)"""
        with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
            for i, table in enumerate(tables):
                if isinstance(table, pd.DataFrame) and not table.empty:
                    # Clean the table
                    table = table.dropna(how='all')
                    table = table.dropna(axis=1, how='all')
                    
                    # Save to sheet
                    sheet_name = f"Table_{i+1}"
                    table.to_excel(writer, sheet_name=sheet_name, index=False)
        
        print(f"✅ Saved {len(tables)} tables to {output_path}")