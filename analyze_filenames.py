import os
import re
from collections import Counter

def classify_filename(filename):
    stem, _ = os.path.splitext(filename)

    # Define known generic patterns
    generic_patterns = {
        "Doxie": re.compile(r"(?i)^Doxie ?\d+"),
        "IMAG": re.compile(r"(?i)^IMAG\d+"),
        "IMG": re.compile(r"(?i)^IMG\d+")
    }

    for label, pattern in generic_patterns.items():
        if pattern.match(stem):
            return label

    return "Original"

def analyze_folder(path):
    summary = Counter()
    try:
        files = os.listdir(path)
        for file in files:
            category = classify_filename(file)
            summary[category] += 1

        total_files = len(files)
        total_generic = summary["Doxie"] + summary["IMAG"] + summary["IMG"]
        total_original = summary["Original"]
        calculated_total = total_generic + total_original

        print(f"\n📁 Scanned folder: {path}")
        print(f"📦 Total files: {total_files}")
        print(f"🧮 Generic filenames: {total_generic}")
        print(f"    - Doxie: {summary['Doxie']}")
        print(f"    - IMAG:  {summary['IMAG']}")
        print(f"    - IMG:   {summary['IMG']}")
        print(f"🖼️ Original filenames: {total_original}")

        if calculated_total == total_files:
            print(f"\n✅ Total check passed: {calculated_total} files accounted for.")
        else:
            print(f"\n⚠️ Mismatch detected:")
            print(f"    Counted: {calculated_total}")
            print(f"    Expected: {total_files}")
            print(f"    Difference: {abs(total_files - calculated_total)}")

    except Exception as e:
        print(f"❌ Error scanning folder: {e}")

if __name__ == "__main__":
    scan_path = r"D:\ZTEMP\orig_scans"
    analyze_folder(scan_path)