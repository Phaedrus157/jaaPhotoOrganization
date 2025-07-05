import os
import re

# Root directory
root_folder = r'D:\prep'
image_extensions = ('.jpg', '.jpeg', '.png', '.heic', '.dng')

# Camera patterns
camera_patterns = [
    r'^IMG_\d{4,}', r'^IMG_\d{4,} \(\d+\)', r'^IMAG\d{4,}', r'^IMAG\d{4,} \(\d+\)',
    r'^P\d{6,}', r'^\d{5,}', r'^DSC[F]?\d{4,}', r'^\d{3}-\d{4}_IMG',
    r'^Picture \d{3}', r'^IMG\d{3,} ?\(\d+\)', r'^\d{3}_\d{4}$',
    r'^\d{3}_\d{4} \(.+?\)$', r'^DSC\d{4,} \(.+?\)$', r'^\d{4} \d{3,4}$',
    r'^Photo\d{3,}_\d{3,}$',
    r'^WP_\d{8}_\d{2}_\d{2}_\d{2}(_[a-zA-Z]+){1,2}( \(\d+\))?$',
    r'^[0-9a-z]{8}_[0-9]{10,}(_[a-zA-Z])?( \(\d+\))?$',  # Flickr-style hashes
]

# Other matchers
doxie_pattern = re.compile(r'^doxie\s*\d+', re.IGNORECASE)
custom_name_pattern = re.compile(r'^(\d+[a-zA-Z]+.*|[a-zA-Z].*)')
hash_pattern = re.compile(r'^[a-f0-9]{32,}( \(\d+\))?$', re.IGNORECASE)
ios_timestamp_pattern = re.compile(r'^(\d{8}_\d+_iOS)( \(\d{4}_\d{2}_\d{2} \d{2}_\d{2}_\d{2} UTC\))?$')

# Counters
category_counts = {
    'Would Rename (generic)': 0,
    'Would Rename (custom)': 0,
    'Would Skip (exists)': 0,
    'Would Resolve Collision': 0,
    'Other': 0
}
rename_log = []
skip_log = []
collision_log = []
folder_counters = {}
total_folders = 0
total_images = 0

print(f"\n🧪 Dry Run: Simulating renaming in {root_folder}\n")

for dirpath, _, files in os.walk(root_folder):
    rel_dir = os.path.relpath(dirpath, root_folder)
    if rel_dir == '.':
        continue

    folder_prefix = rel_dir.replace('\\', '_')
    folder_counters[folder_prefix] = 1
    total_folders += 1

    sorted_files = sorted(f for f in files if f.lower().endswith(image_extensions))

    for file in sorted_files:
        total_images += 1
        original_path = os.path.join(dirpath, file)
        name, ext = os.path.splitext(file)
        rel_path = os.path.relpath(original_path, root_folder)
        cleaned = ''
        category = 'Other'

        match = ios_timestamp_pattern.match(name)
        if match:
            name = match.group(1)
            category = 'Would Rename (generic)'
        elif any(re.match(p, name) for p in camera_patterns):
            category = 'Would Rename (generic)'
        elif doxie_pattern.match(name):
            category = 'Would Rename (generic)'
        elif hash_pattern.match(name):
            category = 'Would Rename (generic)'
        elif custom_name_pattern.match(name):
            category = 'Would Rename (custom)'
            cleaned = re.sub(r'\[.*?\]|\(.*?\)', '', name)
            cleaned = re.sub(r'[^a-zA-Z0-9]', '', cleaned)

        if category == 'Other':
            continue

        counter = folder_counters[folder_prefix]
        folder_counters[folder_prefix] += 1

        if category == 'Would Rename (custom)' and cleaned:
            base_filename = f"{folder_prefix}_{cleaned}_{counter:03d}"
        else:
            base_filename = f"{folder_prefix}_{counter:03d}"

        candidate = os.path.join(dirpath, f"{base_filename}{ext.lower()}")
        suffix = 1
        while os.path.exists(candidate):
            candidate = os.path.join(dirpath, f"{base_filename}_{suffix}{ext.lower()}")
            suffix += 1

        if suffix > 1:
            collision_log.append((rel_path, os.path.relpath(candidate, root_folder)))
            category_counts['Would Resolve Collision'] += 1

        if not os.path.exists(candidate):
            category_counts[category] += 1
            rename_log.append((rel_path, os.path.relpath(candidate, root_folder)))
        else:
            category_counts['Would Skip (exists)'] += 1
            skip_log.append(rel_path)

# Summary
print("📊 Simulated Summary:")
print(f"  Total folders scanned: {total_folders}")
print(f"  Total image files evaluated: {total_images}")
for cat, count in category_counts.items():
    print(f"  {cat}: {count}")

if rename_log:
    print("\n📝 Would Rename:")
    for old, new in rename_log:
        print(f"{old} ➡ {new}")

if collision_log:
    print("\n🔁 Would Resolve Collisions:")
    for original, resolved in collision_log:
        print(f"  {original} ➡ {resolved}")

if skip_log and any(f.strip() for f in skip_log):
    print("\n⚠️ Would Skip (existing destination):")
    for skipped in skip_log:
        print(f"  {skipped}")

print("\n🚫 Dry run complete — no files were renamed or modified.\n")