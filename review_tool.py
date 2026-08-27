import csv
import os
import subprocess
import tempfile
import sys

def open_pdf(pdf_path):
    try:
        subprocess.Popen(["open", "-a", "Google Chrome", pdf_path])
    except Exception as e:
        print(f"Error opening PDF: {e}")

def edit_notes_text(current_text):
    with tempfile.NamedTemporaryFile(suffix=".txt", delete=False, mode="w", encoding="utf-8") as temp_file:
        temp_file.write(current_text)
        temp_path = temp_file.name

    try:
        print("\nOpening TextEdit to edit notes...")
        print("--> Edit the text, SAVE (Cmd+S), and CLOSE (Cmd+W) the TextEdit window to continue...", flush=True)
        subprocess.call(["open", "-W", "-e", temp_path])
        
        with open(temp_path, "r", encoding="utf-8") as f:
            updated_text = f.read().strip()
            
        return updated_text
    except Exception as e:
        print(f"Error during TextEdit call: {e}")
        return current_text
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)

def main():
    BASE = os.path.dirname(os.path.abspath(__file__))
    source_csv = os.path.join(BASE, "report_results_guesses.csv")
    verified_csv = os.path.join(BASE, "report_results_verified.csv")
    
    if not os.path.exists(source_csv):
        print(f"Error: Source CSV not found at {source_csv}")
        print("Please make sure you have run generate_guesses.py to create report_results_guesses.csv.")
        sys.exit(1)
        
    fieldnames = ["year", "file", "inspector", "status", "violations", "notes"]
    
    verified_files = set()
    if os.path.exists(verified_csv):
        try:
            with open(verified_csv, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    verified_files.add((row["year"], row["file"]))
            print(f"Resuming review. Found {len(verified_files)} already verified entries.", flush=True)
        except Exception as e:
            print(f"Error reading verified CSV: {e}. Starting fresh.", flush=True)

    if not os.path.exists(verified_csv):
        with open(verified_csv, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()

    source_rows = []
    with open(source_csv, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            source_rows.append(row)
            
    total_count = len(source_rows)
    print(f"Loaded {total_count} total entries from guesses CSV.", flush=True)
    
    pending_rows = [r for r in source_rows if (r["year"], r["file"]) not in verified_files]
    
    if not pending_rows:
        print("All entries have already been verified!", flush=True)
        sys.exit(0)
        
    print(f"\n{len(pending_rows)} entries pending review. Press Enter key to start...", flush=True)
    input()
    
    for idx, row in enumerate(pending_rows):
        year = row["year"]
        filename = row["file"]
        inspector = row["inspector"]
        status = row["status"]
        violations = row["violations"]
        notes = row["notes"]
        
        pdf_path = os.path.join(BASE, year, filename)
        
        open_pdf(pdf_path)
        
        while True:
            os.system("clear")
            print("="*60)
            print(f"Reviewing [{idx+1}/{len(pending_rows)}] (Total: {total_count})")
            print(f"Year: {year} | File: {filename}")
            print("-" * 60)
            print(f"Inspector: {inspector}")
            print(f"Status   : {status}")
            print(f"Sections : {violations}")
            print("-" * 60)
            print("Notes/Description:")
            print(notes)
            print("="*60)
            print("Commands:")
            print("  [Enter] - Accept and Save")
            print("  i       - Edit Inspector Name")
            print("  s       - Toggle Status (COMPLIANT / NONCOMPLIANT)")
            print("  v       - Edit Violations list (comma-separated standard codes)")
            print("  n       - Edit Notes/Description (opens in TextEdit)")
            print("  q       - Quit tool")
            print("-" * 60)
            
            choice = input("Enter command: ").strip().lower()
            
            if choice == "":
                with open(verified_csv, "a", newline="", encoding="utf-8") as f:
                    writer = csv.DictWriter(f, fieldnames=fieldnames)
                    writer.writerow({
                        "year": year,
                        "file": filename,
                        "inspector": inspector,
                        "status": status,
                        "violations": violations,
                        "notes": notes
                    })
                break
            elif choice == "i":
                new_inspector = input("Enter correct inspector name: ").strip()
                if new_inspector:
                    inspector = new_inspector.title()
            elif choice == "s":
                status = "COMPLIANT" if status == "NONCOMPLIANT" else "NONCOMPLIANT"
                if status == "COMPLIANT":
                    violations = "None"
                    notes = "None"
            elif choice == "v":
                new_violations = input("Enter standard violation codes (e.g. 701.20, 701.130): ").strip()
                if new_violations:
                    violations = new_violations
                    status = "NONCOMPLIANT"
                else:
                    violations = "None"
                    status = "COMPLIANT"
                    notes = "None"
            elif choice == "n":
                notes = edit_notes_text(notes)
            elif choice == "q":
                print("\nQuitting review tool. Your progress is saved.", flush=True)
                sys.exit(0)
            else:
                print("Invalid command. Press Enter to retry...")
                input()

    print("\nAll pending entries have been verified and saved to report_results_verified.csv!", flush=True)

if __name__ == "__main__":
    main()
