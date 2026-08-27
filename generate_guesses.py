import csv
import glob
import os
import re
import sys
import time
import json
import ssl
import urllib.request
import urllib.error
import pdfplumber

DELAY_BETWEEN_REQUESTS = 0.5

def clean_json_response(text):
    text = text.strip()
    if text.startswith("```json"):
        text = text[7:]
    elif text.startswith("```"):
        text = text[3:]
    if text.endswith("```"):
        text = text[:-3]
    return text.strip()

def get_pdf_summary_text(pdf_path):
    try:
        with pdfplumber.open(pdf_path) as pdf:
            n_pages = len(pdf.pages)
            indices = sorted(list(set(list(range(min(3, n_pages))) + list(range(max(0, n_pages - 3), n_pages)))))
            pages_text = []
            for idx in indices:
                text = pdf.pages[idx].extract_text()
                if text:
                    pages_text.append(f"--- PAGE {idx+1} ---\n{text}")
            return '\n'.join(pages_text)
    except Exception as e:
        print(f"Error reading PDF {pdf_path}: {e}", flush=True)
        return ""

def call_gemini_api(prompt, api_key, ssl_context):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.5-flash:generateContent?key={api_key}"
    headers = {"Content-Type": "application/json"}
    
    payload = {
        "contents": [{
            "parts": [{
                "text": prompt
            }]
        }],
        "generationConfig": {
            "responseMimeType": "application/json"
        }
    }
    
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers=headers,
        method="POST"
    )
    
    max_retries = 3
    for attempt in range(max_retries):
        try:
            with urllib.request.urlopen(req, timeout=90, context=ssl_context) as response:
                res_data = response.read().decode("utf-8")
                res_json = json.loads(res_data)
                text_response = res_json['candidates'][0]['content']['parts'][0]['text']
                cleaned_text = clean_json_response(text_response)
                return json.loads(cleaned_text)
        except urllib.error.HTTPError as e:
            if e.code == 429:
                wait_time = 15 * (attempt + 1)
                print(f"\nRate limit hit. Sleeping for {wait_time} seconds before retrying (Attempt {attempt+1}/{max_retries})...", flush=True)
                time.sleep(wait_time)
            else:
                try:
                    err_msg = e.read().decode('utf-8')
                except Exception:
                    err_msg = str(e)
                print(f"\nHTTP Error {e.code}: {err_msg}", flush=True)
                break
        except json.JSONDecodeError as e:
            print(f"\nFailed to parse JSON response: {e}. Raw text was:\n{text_response}", flush=True)
            break
        except Exception as e:
            print(f"\nAPI call error: {e}", flush=True)
            time.sleep(2)
            
    return None

def fallback_regex_extractor(text_content):
    inspector = "NOT FOUND"
    m = re.search(r'(?i)Specialist\s+([A-Z][a-zA-Z.\-\' \t]+)', text_content)
    if m:
        name = m.group(1).split('\n')[0].strip()
        inspector = re.split(r',|\-|–', name)[0].strip().title()
        if inspector == "Rawlings":
            inspector = "Stephanie Rawlings"
            
    violations = sorted(list(set(re.findall(r'\b701\.\d+\b', text_content))))
    
    status = "COMPLIANT"
    violations_str = "None"
    
    if violations:
        status = "NONCOMPLIANT"
        violations_str = ", ".join(violations)
        
    return {
        "inspector": inspector,
        "status": status,
        "violations": violations_str,
        "notes": "Extracted via Fallback Regex"
    }

def main():
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("Error: GEMINI_API_KEY environment variable is not set.", flush=True)
        print("Please obtain a free API key from https://aistudio.google.com/ and set it in your terminal:", flush=True)
        print("export GEMINI_API_KEY='your_api_key_here'", flush=True)
        sys.exit(1)
        
    BASE = os.path.dirname(os.path.abspath(__file__))
    year_dirs = sorted(
        d for d in os.listdir(BASE)
        if os.path.isdir(os.path.join(BASE, d)) and d.isdigit()
    )
    
    csv_path = os.path.join(BASE, "report_results_guesses.csv")
    fieldnames = ["year", "file", "inspector", "status", "violations", "notes"]
    
    processed_files = set()
    if os.path.exists(csv_path):
        try:
            with open(csv_path, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    processed_files.add((row["year"], row["file"]))
            print(f"Resuming run. Found {len(processed_files)} files already processed in {csv_path}", flush=True)
        except Exception as e:
            print(f"Error reading existing CSV: {e}. Starting fresh.", flush=True)
            
    if not processed_files:
        with open(csv_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            
    ssl_context = ssl._create_unverified_context()
    
    all_pdfs = []
    for year in year_dirs:
        pdf_paths = sorted(glob.glob(os.path.join(BASE, year, "*.pdf")))
        for pdf_path in pdf_paths:
            filename = os.path.basename(pdf_path)
            all_pdfs.append((year, filename, pdf_path))
            
    total_count = len(all_pdfs)
    pending_pdfs = [p for p in all_pdfs if (p[0], p[1]) not in processed_files]
    
    if not pending_pdfs:
        print("\nAll files have already been processed!", flush=True)
        sys.exit(0)
        
    print(f"\nProcessing {len(pending_pdfs)} pending files (Total: {total_count})...", flush=True)
    
    for idx, (year, filename, pdf_path) in enumerate(pending_pdfs):
        print(f"  [{idx+1}/{len(pending_pdfs)}] Processing {year}/{filename}...", end="", flush=True)
        
        text_content = get_pdf_summary_text(pdf_path)
        if not text_content:
            inspector = "PORTFOLIO (Unreadable)"
            status = "PORTFOLIO (Unreadable)"
            violations = "PORTFOLIO (Unreadable)"
            notes = "Portfolio wrapper detected"
        else:
            prompt = f"""
You are an expert compliance auditor. Analyze the following extracted text from an Illinois County Jail Inspection/Monitoring Report.
Your task is to extract:
1. The name of the inspector/specialist who signed the report (usually printed above their signature block near the end of the report summary). Normalize to Title Case (e.g. 'Kathy Melvin').
2. The compliance status of the jail:
   - "COMPLIANT" if there are absolutely NO standard noncompliances listed under the Noncompliances section.
   - "NONCOMPLIANT" if there are listed standard violations or noncompliances.
3. The list of specific section code numbers that were violated. These section numbers are in the format "701.XX" (e.g. "701.130", "701.80", "701.20").
   - Output them as a clean comma-separated list (e.g., "701.20, 701.130, 701.80").
   - If status is "COMPLIANT", return "None".
4. A brief, concise description summarizing the violations. If status is "COMPLIANT", return "None".

Here is the extracted text:
{text_content}

Output the result in the following JSON format ONLY:
{{
  "inspector": "Inspector Name or 'NOT FOUND'",
  "status": "COMPLIANT or NONCOMPLIANT",
  "violations": "None or '701.20, 701.130'",
  "notes": "Brief notes/descriptions or 'None'"
}}
"""
            result = call_gemini_api(prompt, api_key, ssl_context)
            if result:
                inspector = result.get("inspector", "NOT FOUND")
                status = result.get("status", "COMPLIANT")
                violations = result.get("violations", "None")
                notes = result.get("notes", "None")
            else:
                print(" API Call failed. Running fallback regex parser...", end="", flush=True)
                fallback = fallback_regex_extractor(text_content)
                inspector = fallback["inspector"]
                status = fallback["status"]
                violations = fallback["violations"]
                notes = fallback["notes"]
        
        with open(csv_path, "a", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writerow({
                "year": year,
                "file": filename,
                "inspector": inspector,
                "status": status,
                "violations": violations,
                "notes": notes
            })
            f.flush()
            
        print(" Done.", flush=True)
        
        time.sleep(DELAY_BETWEEN_REQUESTS)
        
    print(f"\nDone! All files processed. Results saved to {csv_path}", flush=True)

if __name__ == "__main__":
    main()
