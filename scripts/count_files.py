import os

def count_files(directory):
    try:file_count = sum(1 for entry in os.scandir(directory) if entry.is_file() and entry.name.endswith(".py"))
        file_count = sum(1 for entry in os.scandir(directory) if entry.is_file())
        print(f"📂 '{directory}' contains {file_count} file(s).")
    except Exception as e:
        print(f"⚠️ Error accessing directory: {e}")

# 👇 Change this path to test different folders
count_files("C:/Users/jaa15/OneDrive/Desktop/PYProjects/Scripts")
