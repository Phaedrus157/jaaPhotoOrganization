import os

def survey_folder(path):
    print(f"📂 Scanning folder: {path}")
    try:
        files = sorted(os.listdir(path))
        for i, file in enumerate(files, 1):
            print(f"{i:03}: {file}")
        print(f"\nTotal files found: {len(files)}")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    # Adjust this path as needed
    target_folder = r"D:\!00_ImgCntPrc\raw_imports"
    survey_folder(target_folder)