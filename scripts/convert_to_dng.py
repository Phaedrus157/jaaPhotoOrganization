import os
import subprocess

def convert_to_dng(src, converter_path):
    try:
        files = [f for f in os.listdir(src) if f.lower().endswith(".cr2")]
        for file in files:
            full_path = os.path.join(src, file)
            cmd = [
                converter_path,
                "-c",          # Use compression
                "-p1",         # Preserve subfolders
                "-o", src,     # Output folder (same as source for now)
                full_path
            ]
            print(f"🔄 Converting: {file}")
            subprocess.run(cmd, check=True)
        print(f"\n✅ Converted {len(files)} files to DNG")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    source_folder = r"D:\!00_ImgCntPrc\active_catalog\by_date"
    dng_converter = r"C:\Program Files\Adobe\Adobe DNG Converter.exe"
    convert_to_dng(source_folder, dng_converter)