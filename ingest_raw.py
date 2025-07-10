import os
import shutil
from datetime import datetime

def ingest_files(src, dest_base, use_date=True):
    try:
        files = [f for f in os.listdir(src) if f.endswith(".CR2")]
        for file in files:
            timestamp = datetime.now().strftime("%Y-%m-%d")
            subfolder = "by_date" if use_date else "by_project"
            dest_folder = os.path.join(dest_base, subfolder, timestamp)
            os.makedirs(dest_folder, exist_ok=True)

            src_path = os.path.join(src, file)
            dest_path = os.path.join(dest_folder, file)
            shutil.move(src_path, dest_path)
            print(f"📦 Moved: {file} → {dest_folder}")

        print(f"\n✅ Ingested {len(files)} files into {subfolder}/{timestamp}")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    source = r"D:\!00_ImgCntPrc\raw_imports"
    destination = r"D:\!00_ImgCntPrc\active_catalog"
    ingest_files(source, destination, use_date=True)