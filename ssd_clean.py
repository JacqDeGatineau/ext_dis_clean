import os
import hashlib
import sys
import shutil

def hashfile(filename, fast=True):
    try:
        if 'Backups.backupdb' in filename or filename.startswith('/Volumes/.timemachine'):
            print(f"Skipping Time Machine file: {filename}")
            return None # skip time machine backups

        if os.path.isdir(filename) or filename.startswith('.'):
            return None  # Skip directories and system files
        
        hasher = hashlib.md5() # not cryptographically secure, but ok for file checksums
        with open (filename, "rb") as f:
            if fast:
                data = f.read(8192) #read first 8kb first to fasten the hashing
                hasher.update(data)
            else:
                while True:
                    data = f.read(1024)
                    if not data:
                        break
                    hasher.update(data)
            return hasher.hexdigest()
    except Exception as e:
        print(f"Error hashing file {filename}: {e}")
        return None

def get_all_files(directory):
    files = []
    for root, dirnames, filenames in os.walk(directory):
        print(f"Checking {root}")
        dirnames[:] = [
            d for d in dirnames 
            if 'Backups.backupdb' not in d 
            and not d.startswith('.Apple')
        ]
        for filename in filenames:
            files.append(os.path.join(root, filename))
        for dirname in dirnames:
            files.append(os.path.join(root, dirname))
    return files

def find_duplicates(dir_1, dir_2):
    dir_1_files = get_all_files(dir_1)
    dir_2_files = get_all_files(dir_2)

    hash_cache = {}
    duplicates = []
    to_remove = []

    #get hash with caching
    def get_file_hash(file):
        if file in hash_cache:
            return hash_cache[file]
        file_hash = hashfile(file)
        if file_hash:
            hash_cache[file] = file_hash
        return file_hash

    dir_1_hashes = {get_file_hash(file): file for file in dir_1_files}

    for file in dir_2_files:
        file_hash = get_file_hash(file)
        if file_hash in dir_1_hashes:
            duplicates.append((dir_1_hashes[file_hash], file))
            to_remove.append(file)

    return duplicates, to_remove

def record(dupl):
    output_file = "duplicates.txt"
    with open(output_file, "w") as file:
        print(f"{len(dupl)} duplicates found")
        file.write(f"Found {len(dupl)} duplicate files: \n\n")
        for d in dupl:
            print(f"File: {d[0]}\nDuplicate: {d[1]}")
            file.write(f"File: {d[0]}\nDuplicate: {d[1]}\n\n")
   

def remove_duplicates(to_remove, disk2_path):
    remove = input("Do you want to remove duplicates? Y/N: ")
    record = "removed.txt"
    if remove == "Y":
        for item in to_remove:
            if os.path.isfile(item):
                os.remove(item)

        for item in sorted(to_remove, key=len, reverse=True):  # Sort by path length, deepest paths first
            if os.path.isdir(item):
                if not os.listdir(item):  #Check whether empty
                    shutil.rmtree(item)

        print(f"{len(to_remove)} duplicates were removed from {disk2_path}")
        with open(record, "w") as file:
            file.write(f"Duplicate files removed: \n\n")
            for item in to_remove:
                file.write(item + "\n")
    else:
        print("OK Daddy-O!")
    

if __name__ == "__main__":
    disk1_path = (".")
    disk2_path = "path"

    if not os.path.isdir(disk1_path):
        print(f"Error: Directory '{disk1_path}' does not exist or is not a valid directory.")
        sys.exit(1)
    if not os.path.isdir(disk2_path):
        print(f"Error: Directory '{disk2_path}' does not exist or is not a valid directory.")
        sys.exit(1)

    duplicates, to_remove = find_duplicates(disk1_path, disk2_path)
    
    if duplicates:
        record(duplicates)
        remove_duplicates(to_remove, disk2_path)
    else:
        print("No duplicate files found.")


