import csv
import glob
import os
import re
import pdfplumber

# Constants for recognized specialist/inspector titles
TITLES = [
    'Criminal Justice Specialist', 'Jail and Detention Standards', 
    'CJSII', 'CJS II', 'CJS', 'JDSU', 'Manager', 'Inspector', 'Compliance Monitor'
]

def clean_name(name_str):
    """Normalize and clean the inspector name string."""
    name_str = name_str.strip()
    name_str = name_str.replace('_', '')
    # Split by comma or dashes
    name_str = re.split(r',|\-|–', name_str)[0].strip()
    # Remove prefix titles
    name_str = re.sub(
        r'^(?:Specialist|Criminal Justice Specialist|Manager|CJSII|CJS II|CJS|JDSU|Standards Unit Manager|Inspector|Compliance Monitor)\s+', 
        '', name_str, flags=re.I
    )
    # Remove curly and double quotes
    name_str = name_str.replace('“', '').replace('”', '').replace('\"', '')
    return name_str.strip().title()

def find_inspector(pdf):
    """Attempt to find the inspector's name on the last two pages or page 1 fallback."""
    # Check the last page first, then the penultimate page
    pages_to_check = [pdf.pages[-1]]
    if len(pdf.pages) > 1:
        pages_to_check.append(pdf.pages[-2])
        
    for page in pages_to_check:
        text = page.extract_text() or ''
        lines = [l.strip() for l in text.split('\n') if l.strip()]
        for idx in reversed(range(len(lines))):
            line = lines[idx]
            # Ignore long lines (sentences) and department names ending in 'Unit'
            if len(line) > 60:
                continue
            if line.endswith('Unit') or line.endswith('Unit.'):
                if not line.startswith(('Inspector', 'Manager', 'Specialist', 'Compliance Monitor')):
                    continue
            if any(w in line.lower() for w in ['monitored', 'inspected', 'reviewed', 'conducted', 'entrance', 'exit', 'distribution:', 'comment']):
                continue
                
            if any(t in line for t in TITLES):
                # Check for "Name, Title" pattern on the same line
                m = re.match(r'^([A-Z][a-zA-Z.\-\' \t“”\"]+),\s*(?:CJSII|CJS II|Criminal Justice Specialist|Jail|Manager|JDSU|CJS|Inspector|Compliance Monitor)', line, re.I)
                if m:
                    name = clean_name(m.group(1))
                    if name not in TITLES:
                        return name
                # Check for the name on the line immediately above the title
                if idx > 0:
                    prev = lines[idx-1]
                    prev_lines = prev.split('\n')
                    if prev_lines:
                        cleaned = clean_name(prev_lines[-1])
                        if cleaned in TITLES or cleaned in ['County Clerk', 'County Board Chairman']:
                            continue
                        if len(cleaned) < 50 and re.match(r'^[A-Z][a-zA-Z.\-\' \t“”\"]+$', cleaned):
                            return cleaned
                            
    # Fallback to page 1 for older cover-letters referencing 'Specialist <Name>'
    page1_text = pdf.pages[0].extract_text() or ''
    m = re.search(r'(?i)Specialist\s+([A-Z][a-zA-Z.\-\' \t“”\"]+)', page1_text)
    if m:
        name = clean_name(m.group(1))
        # Map raw abbreviation Rawlings to Stephanie Rawlings
        if name == 'Rawlings':
            return 'Stephanie Rawlings'
        return name
        
    if 'PDF portfolio' in page1_text or 'Acrobat' in page1_text:
        return 'PORTFOLIO (Unreadable)'
        
    return 'NOT FOUND'

def extract_noncompliances(pdf, inspector_name):
    """Extract noncompliances section content or return 'None'."""
    # Scan the entire document page-by-page from the beginning
    pages_text = []
    for page in pdf.pages:
        pages_text.append(page.extract_text() or '')
    full_text = '\n'.join(pages_text)
    
    # Locate the noncompliance section header (highly permissive for typos and variants)
    # Matches NONCOMPLIANCES / NON-COMPLIANCES / NONCOMPLIANCE'S
    # Followed optionally by WITH (THE) ILLINOIS COUNTY JAIL STANDARDS (allowing spacing issues and typos like SANDARDS)
    match = re.search(r'(?i)noncompliance[’\']?s?(?:\s*with\s*(?:the\s*)?illinois\s*county\s*jail\s*s[ta]*[nd]+ards)?\s*(.*)', full_text, re.DOTALL)
    if not match:
        # Check if portfolio wrapper
        page1_text = pages_text[0] if pages_text else ''
        if 'PDF portfolio' in page1_text or 'Acrobat' in page1_text:
            return 'PORTFOLIO (Unreadable)'
        return 'None'
        
    remaining_text = match.group(1)
    lines = remaining_text.split('\n')
    noncompliance_lines = []
    
    for line in lines:
        clean_line = line.strip()
        if not clean_line:
            noncompliance_lines.append(line)
            continue
            
        # Check stop words indicating the absolute end of the report summary
        if any(stop_word in clean_line.lower() for stop_word in [
            'distribution:', 
            'county jail inspection checklist'
        ]):
            break
            
        # Skip/ignore page headers and footers rather than breaking the loop,
        # so that subsequent pages continue to be read.
        if any(skip_word in clean_line.lower() for skip_word in [
            'mission: to serve', 
            'www.illinois.gov',
            'illinois department of corrections',
            'office of jail and detention standards'
        ]):
            if 'office of jail and detention standards' in clean_line.lower() and not clean_line.endswith('Unit'):
                # Check if it's the signature block title or the page header
                if len(clean_line) < 45:
                    break
            continue
            
        if clean_line.isdigit():  # Skip page numbers, don't stop the loop
            continue
            
        if inspector_name and inspector_name.lower() in clean_line.lower():
            # Only break if it looks like a signature block line (not a long sentence referencing the inspector)
            if len(clean_line) < 40 and not any(w in clean_line.lower() for w in ['monitored', 'inspected', 'reviewed', 'conducted', 'entrance', 'exit']):
                break
            
        if any(title.lower() in clean_line.lower() for title in [
            'criminal justice specialist', 
            'jail and detention standards'
        ]):
            # Only break if it looks like a signature block title line (short)
            if len(clean_line) < 45:
                break
            
        noncompliance_lines.append(line)
        
    extracted = '\n'.join(noncompliance_lines).strip()
    
    # Post-extraction validation: check if the substance is just empty or variations of 'none'
    # E.g., 'None', 'NONE', 'Recommendations\nNone', 'Recommendations:\nNone'
    clean_extracted = re.sub(r'(?i)recommendations?:?\s*\bnone\b', '', extracted).strip()
    clean_extracted = re.sub(r'(?i)\bnone\b|\bno\b|\bn/a\b', '', clean_extracted).strip()
    
    # If after removing 'None' and 'Recommendations None' there is no actual text left, return 'None'
    if not clean_extracted:
        return 'None'
        
    return extracted

def main():
    BASE = os.path.dirname(os.path.abspath(__file__))
    # Find all digits subfolders (e.g. 2017, 2018, ...)
    year_dirs = sorted(
        d for d in os.listdir(BASE)
        if os.path.isdir(os.path.join(BASE, d)) and d.isdigit()
    )
    
    csv_path = os.path.join(BASE, "report_results.csv")
    fieldnames = ["year", "file", "inspector", "noncompliances"]
    
    # Open CSV in write mode and write header/each row on the fly to save memory
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        f.flush()
        
        total_count = 0
        for year in year_dirs:
            pdf_paths = sorted(glob.glob(os.path.join(BASE, year, "*.pdf")))
            print(f"Processing year {year} ({len(pdf_paths)} PDFs)...", flush=True)
            for pdf_path in pdf_paths:
                filename = os.path.basename(pdf_path)
                try:
                    with pdfplumber.open(pdf_path) as pdf:
                        inspector = find_inspector(pdf)
                        noncompliances = extract_noncompliances(pdf, inspector)
                except Exception as e:
                    print(f"  Error reading {year}/{filename}: {e}", flush=True)
                    inspector = "ERROR (Failed to read)"
                    noncompliances = "ERROR"
                    
                writer.writerow({
                    "year": year,
                    "file": filename,
                    "inspector": inspector,
                    "noncompliances": noncompliances
                })
                f.flush()
                total_count += 1
                
        print(f"\nDone! Processed {total_count} reports. Results saved to {csv_path}", flush=True)

if __name__ == "__main__":
    main()
