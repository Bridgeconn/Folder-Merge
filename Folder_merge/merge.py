import os
import shutil
import ffmpeg
import subprocess

# To find unique prefixes in the base directory

def find_unique_prefixes(base_dir):
    unique_prefixes = set()
    for item in os.listdir(base_dir):
        
        
        if os.path.isdir(os.path.join(base_dir, item)):
            unique_prefixes.add(item[:3].upper())
   
    return list(unique_prefixes)


# To find directories in the base directory that start with a given prefix

def find_dirs_with_prefix(base_dir, prefix):
    
    dirs_with_prefix = []
    for item in os.listdir(base_dir):
        lang_dir = os.path.join(base_dir, item)
        
        
        if os.path.isdir(lang_dir) and item[:3].upper() == prefix:
            
            dirs_with_prefix.append(lang_dir)
    
    return dirs_with_prefix

# To find subdirectories within a specified subfolder

def find_source_dirs(base_dir, subfolder_name):
    source_dirs = []
    base_subfolder = os.path.join(base_dir, subfolder_name)
   
    if os.path.exists(base_subfolder):
        for item in os.listdir(base_subfolder):
            
            candidate = os.path.join(base_subfolder, item)
            if os.path.isdir(candidate):
                source_dirs.append(candidate)
   
    return source_dirs

# Copy files from source directory to destination directory

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



# Count the number of chapters in the output directory

def count_chapters(prefix, output_dir):
    luk_dir = os.path.join(output_dir, f'Merged_without_conversion/{prefix}/LUK')
    if not os.path.exists(luk_dir):
        return 0

    chapters = [chapter for chapter in os.listdir(luk_dir) if os.path.isdir(os.path.join(luk_dir, chapter))]
    return (chapters)

# Count the no of chapters in the specific chapter directory

def count_files_in_chapter(prefix, chapterno, output_dir):
    chapter_dir = os.path.join(output_dir, f'Merged_without_conversion/{prefix}/LUK/{chapterno}')
    if not os.path.exists(chapter_dir):
        return 0

    files = [file for file in os.listdir(chapter_dir) if os.path.isfile(os.path.join(chapter_dir, file))]
    return len(files)

# check duplicate chapters across directories with the same prefix

def check_for_duplicates(prefix, subfolder_name,dirs_with_prefix):
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

# function to merge folders

def merge_folders(base_dir, subfolder_name, output_dir):

    merge_results=[]

    unique_prefixes = find_unique_prefixes(base_dir)
    chapter_counts = {prefix: 0 for prefix in unique_prefixes}
    
    for prefix in unique_prefixes:
        target_base_dir = os.path.join(output_dir, f'Merged_without_conversion/{prefix}/LUK')
        if not os.path.exists(target_base_dir):
            os.makedirs(target_base_dir)
        
        dirs_with_prefix = find_dirs_with_prefix(base_dir, prefix)
        
        duplicates = check_for_duplicates(prefix,subfolder_name,dirs_with_prefix) 
        
    
        if duplicates:
            merge_results.append((f"Duplicate chapters found in {prefix}:"))
            for chapterno, paths in duplicates.items():
                merge_results.append(f"  Chapter {chapterno} found in {paths}")

        chapter_suffix_counter={}
        
        for dir_with_prefix in dirs_with_prefix:
            source_dirs = find_source_dirs(dir_with_prefix, subfolder_name)
            for src_dir in source_dirs:

                chapterno = os.path.basename(src_dir)
             
              # For duplicate chapters,append a suffix to the chapterno 

                if chapterno not in chapter_suffix_counter:
                    chapter_suffix_counter[chapterno] = 0
                else:
                    chapter_suffix_counter[chapterno]+=1
               

                if chapter_suffix_counter[chapterno] == 0:
                    unique_chapter_no=chapterno
                else:
                    suffix=f"duplicate_{chapter_suffix_counter[chapterno]}"
                    unique_chapter_no=f"{chapterno}_{suffix}"
                
               
                dest_dir = os.path.join(target_base_dir, unique_chapter_no)
                
                if os.path.commonpath([src_dir, output_dir]) == output_dir:
                    continue
                
                file_count = copy_files(src_dir, dest_dir)
                chapter_counts[prefix] += 1 
    
    print("Files merged successfully!")
    for prefix in unique_prefixes:
        chapters = count_chapters(prefix, output_dir)
        total_chapters=len(chapters)
        merge_results.append((f"{prefix}: {total_chapters} chapters"))
        for chapterno in chapters:
            chapter_files_count = count_files_in_chapter(prefix, str(chapterno), output_dir)
            merge_results.append(f"  Chapter {chapterno}: {chapter_files_count} files")
    
    result_file_path=os.path.join(output_dir,"report.txt")
    with open(result_file_path,"w") as f:
       for line in merge_results:
           f.write(line + "\n")

    return merge_results


# convert the files to mp3 after merging

def convert_to_mp3(output_dir):
    merged_dir=os.path.join(output_dir,"Merged_without_conversion")
    converted_dir=os.path.join(output_dir,"Merged and Converted")
    for root,dirs,files in os.walk(merged_dir):
        for file in files:
            src_file=os.path.join(root,file)
            rel_path=os.path.relpath(root,merged_dir)
            dest_dir=os.path.join(converted_dir,rel_path)
            if not os.path.exists(dest_dir):
                os.makedirs(dest_dir)
           
            dest_file=os.path.join(dest_dir,os.path.splitext(file)[0])
            ffmpeg.input(src_file).output(dest_file,format='mp3').run() 
            file_format=check_file_format(dest_file)
            print(f"file_format after conversion {file_format}")



# check the file format after conversion
            
def check_file_format(file_path):
    result = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=format_name', '-of', 'default=noprint_wrappers=1:nokey=1', file_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return result.stdout.decode().strip()

     
         