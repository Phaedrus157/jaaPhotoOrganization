import os
import re
from collections import Counter

def is_generic(filename):
    stem, _ = os.path.splitext(filename)
    patterns = [
        re.compile(r"(?i)^Doxie ?\d+"),
        re.compile(r"(?i)^IMAG\d+")
        # IMG is excluded for now since none were found
    ]
    return any(p.match(stem) for p in patterns)

def simulate_rename(path, prefix="SCAN_"):
    try:
        files = [f for f in os.listdir(path) if is_generic(f)]
        files_sorted = sorted(files)
        print(f"\n📁 Dry-run rename in: {path}")
        print(f"🔍 Found {len(files_sorted)} generic files to rename:\n")

        for i, file in enumerate(files_sorted, 1):
            ext = os.path.splitext(file)[1]
            new_name = f"{prefix}{i:04}{ext.lower()}"
            print(f"→ {file}  →  {new_name}")

        print(f"\n✅ Dry-run complete. No changes were made.")

    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    target_path = r"D:\ZTEMP\orig_scans"
    simulate_rename(target_path)