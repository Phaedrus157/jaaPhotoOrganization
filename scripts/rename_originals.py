import os

def rename_files(path, prefix="IMG_", extension=".CR2"):
    try:
        files = [f for f in os.listdir(path) if f.endswith(extension)]
        for i, file in enumerate(sorted(files), 1):
            new_name = f"{prefix}{i:04}{extension}"
            old_path = os.path.join(path, file)
            new_path = os.path.join(path, new_name)
            os.rename(old_path, new_path)
            print(f"✅ Renamed: {file} → {new_name}")
        print(f"\n🔁 Renamed {len(files)} files in {path}")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    folder_to_rename = r"D:\!00_ImgCntPrc\raw_imports"
    rename_files(folder_to_rename)