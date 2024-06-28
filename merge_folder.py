import os
import shutil

base_dir = ''
subfolder_name = 'ingredients/LUK'
output_dir = os.path.join(base_dir, 'output')

def find_unique_prefixes(base_dir):
    unique_prefixes = set()
    for item in os.listdir(base_dir):
        if os.path.isdir(os.path.join(base_dir, item)):
            unique_prefixes.add(item[:3].upper())
    return list(unique_prefixes)

def find_dirs_with_prefix(base_dir, prefix):
    dirs_with_prefix = []
    for item in os.listdir(base_dir):
        candidate = os.path.join(base_dir, item)
        if os.path.isdir(candidate) and item[:3].upper() == prefix:
            dirs_with_prefix.append(candidate)
    return dirs_with_prefix

def find_source_dirs(base_dir, subfolder_name):
    source_dirs = []
    base_subfolder = os.path.join(base_dir, subfolder_name)
    if os.path.exists(base_subfolder):
        for item in os.listdir(base_subfolder):
            candidate = os.path.join(base_subfolder, item)
            if os.path.isdir(candidate):
                source_dirs.append(candidate)
    return source_dirs

def copy_files(src, dest):
    file_count = 0
    for root, dirs, files in os.walk(src):
        for file in files:
            src_file = os.path.join(root, file)
            dest_file = os.path.join(dest, file)
            dest_dir = os.path.dirname(dest_file)
            if not os.path.exists(dest_dir):
                os.makedirs(dest_dir)
            shutil.copy2(src_file, dest_file)
            file_count += 1
    return file_count

def count_chapters(prefix, output_dir):
    luk_dir = os.path.join(output_dir, f'Merged/{prefix}/LUK')
    if not os.path.exists(luk_dir):
        return 0

    chapters = [chapter for chapter in os.listdir(luk_dir) if os.path.isdir(os.path.join(luk_dir, chapter))]
    return len(chapters)

def count_files_in_chapter(prefix, chapterno, output_dir):
    chapter_dir = os.path.join(output_dir, f'Merged/{prefix}/LUK/{chapterno}')
    if not os.path.exists(chapter_dir):
        return 0

    files = [file for file in os.listdir(chapter_dir) if os.path.isfile(os.path.join(chapter_dir, file))]
    return len(files)

def check_for_duplicates(prefix, dirs_with_prefix):
    chapter_tracker = {}
    for dir_with_prefix in dirs_with_prefix:
        source_dirs = find_source_dirs(dir_with_prefix, subfolder_name)
        for src_dir in source_dirs:
            chapterno = os.path.basename(src_dir)
            if chapterno not in chapter_tracker:
                chapter_tracker[chapterno] = []
            chapter_tracker[chapterno].append(dir_with_prefix)

    duplicates = {chapterno: paths for chapterno, paths in chapter_tracker.items() if len(paths) > 1}
    return duplicates

unique_prefixes = find_unique_prefixes(base_dir)
chapter_counts = {prefix: 0 for prefix in unique_prefixes}

for prefix in unique_prefixes:
    target_base_dir = os.path.join(output_dir, f'Merged/{prefix}/LUK')
    if not os.path.exists(target_base_dir):
        os.makedirs(target_base_dir)
    
    dirs_with_prefix = find_dirs_with_prefix(base_dir, prefix)

    duplicates = check_for_duplicates(prefix, dirs_with_prefix)
    
    if duplicates:
        print(f"Duplicate chapters found for prefix {prefix}:")
        for chapterno, paths in duplicates.items():
            print(f"  Chapter {chapterno} found in {paths}")
    
    for dir_with_prefix in dirs_with_prefix:
        source_dirs = find_source_dirs(dir_with_prefix, subfolder_name)
        for src_dir in source_dirs:
            chapterno = os.path.basename(src_dir)
            
            if chapterno in duplicates:
                
                continue

            dest_dir = os.path.join(target_base_dir, chapterno)
            file_count = copy_files(src_dir, dest_dir)
            chapter_counts[prefix] += 1 

print("Files merged successfully!")
for prefix in unique_prefixes:
    total_chapters = count_chapters(prefix, output_dir)
    print(f"{prefix}: {total_chapters} chapters")
    for chapterno in range(1, total_chapters + 1):
        chapter_files_count = count_files_in_chapter(prefix, str(chapterno), output_dir)
        print(f"  Chapter {chapterno}: {chapter_files_count} files")
