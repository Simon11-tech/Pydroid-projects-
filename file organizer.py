import os
import shutil

# Ask user for the folder path
SOURCE_FOLDER = input("Enter the full folder path to organize: ").strip()

# File type mapping
FILE_TYPES = {
    'Images': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg'],
    'Videos': ['.mp4', '.mov', '.avi', '.mkv'],
    'Documents': ['.pdf', '.doc', '.docx', '.txt', '.xls', '.xlsx', '.ppt', '.pptx'],
    'Music': ['.mp3', '.wav', '.aac', '.flac'],
    'Archives': ['.zip', '.rar', '.tar', '.gz', '.7z'],
    'Scripts': ['.py', '.js', '.html', '.css', '.php'],
    'Executables': ['.apk', '.exe', '.msi'],
    'Others': []
}

def get_folder_name(extension):
    for folder, extensions in FILE_TYPES.items():
        if extension.lower() in extensions:
            return folder
    return 'Others'

def organize_folder(path):
    if not os.path.isdir(path):
        print("❌ Invalid folder path.")
        return

    files_moved = 0

    for filename in os.listdir(path):
        full_path = os.path.join(path, filename)
        if os.path.isfile(full_path):
            _, ext = os.path.splitext(filename)
            folder_name = get_folder_name(ext)
            target_folder = os.path.join(path, folder_name)

            if not os.path.exists(target_folder):
                os.makedirs(target_folder)

            shutil.move(full_path, os.path.join(target_folder, filename))
            files_moved += 1

    print(f"✅ Done! {files_moved} files organized in '{path}'")

# Run
organize_folder(SOURCE_FOLDER)