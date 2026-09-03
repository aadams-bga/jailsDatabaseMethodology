import os
from PyPDF2 import PdfReader

def count_pdf_pages_in_directory(root_dir):
    total_files = 0
    total_pages = 0
    
    print(f"Searching for PDF files in: {root_dir}\n")

    for dirpath, dirnames, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.lower().endswith('.pdf'):
                filepath = os.path.join(dirpath, filename)
                try:
                    with open(filepath, 'rb') as f:
                        reader = PdfReader(f)
                        num_pages = len(reader.pages)
                        total_pages += num_pages
                        total_files += 1
                        print(f"  Found: '{filepath}' ({num_pages} pages)")
                except Exception as e:
                    print(f"  Error reading '{filepath}': {e}")
    
    print(f"Total PDF files found: {total_files}")
    print(f"Total pages across all PDFs: {total_pages}")
    
    return total_files, total_pages

directory_to_scan = '.'
count_pdf_pages_in_directory(directory_to_scan)

