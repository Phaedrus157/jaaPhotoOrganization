import os
import re

def is_generic(filename):
    stem, _ = os.path.splitext(filename)
    patterns = [
        re.compile(r"(?i)^Doxie ?\d+"),
        re.compile(r"(?i)^IMG[_ ]?\d+")
    ]
    if re.match(r"(?i)^SCAN_\d+", stem):
        return False
    return any(p.match(stem) for p in patterns)

def perform_rename(path, prefix="SCAN_"):
    try:
        start_index = 5700  # Start after SCAN_5699
        files = [f for f in os.listdir(path) if is_generic(f)]
        files_sorted = sorted(files)
        print(f"\n🛠️ Renaming {len(files_sorted)} generic files in: {path}\n")

        for i, file in enumerate(files_sorted, start_index):
            ext = os.path.splitext(file)[1]
            new_name = f"{prefix}{i:04}{ext.lower()}"
            old_path = os.path.join(path, file)
            new_path = os.path.join(path, new_name)

            if os.path.exists(new_path):
                print(f"⚠️ Skipped: {file} → {new_name} (already exists)")
                continue

            os.rename(old_path, new_path)
            print(f"✔️ Renamed: {file} → {new_name}")

        print(f"\n✅ Rename complete. IMG files numbered from SCAN_{start_index:04} upward.")

    except Exception as e:
        print(f"❌ Error during rename: {e}")

if __name__ == "__main__":
    target_path = r"D:\ZTEMP\camera_imports"
    perform_rename(target_path)