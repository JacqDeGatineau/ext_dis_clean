import sys
import os
import ssd_clean

disk1_path = input("Insert path to a disk or file with the originals: ")
disk2_path = input("Insert path to a disk or file with files that will be removed: ")

if not os.path.isdir(disk1_path):
    print(f"Error: Directory '{disk1_path}' does not exist or is not a valid directory.")
    sys.exit(1)
if not os.path.isdir(disk2_path):
    print(f"Error: Directory '{disk2_path}' does not exist or is not a valid directory.")
    sys.exit(1)

duplicates, to_remove = ssd_clean.find_duplicates(disk1_path, disk2_path)

if duplicates:
    print(duplicates)
    ssd_clean.record(duplicates)
    ssd_clean.remove_duplicates(to_remove, disk2_path)
else:
    print("No duplicate files found.")
